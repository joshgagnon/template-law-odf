from __future__ import print_function
import signal
import subprocess
import logging
from flask import Flask, request, send_file
from flask import jsonify
import os
import os.path
from io import BytesIO
import tempfile
from subprocess import Popen, STDOUT
import shutil
import errno
from render import render_odt

try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

logging.basicConfig()

PORT = 5668
SOFFICE_BIN = 'soffice'
SOFFICE_PYTHON = 'python3'
CONVERTER = 'DocumentConverter.py'


app = Flask(__name__)


MIMETYPES = {
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'odt': 'application/vnd.oasis.opendocument.text',
    'pdf': 'application/pdf',
    "png": "image/png",
    "html": "text/html",
}

EXTENSIONS = {
    'pdf': '.pdf',
    'odt': '.odt',
    'docx': '.docx',
    'png': '.png',
    'html': '.html'
}



def convert_type(data, type):
    env_path = tempfile.mkdtemp()

    try:
        with tempfile.NamedTemporaryFile(suffix='.odt') as temp_in:
            temp_in.write(data)
            temp_in.flush()
            args = [SOFFICE_BIN, "-env:UserInstallation=file://%s" % env_path, "--headless",
                 "--invisible", "--convert-to", type,  "--outdir", env_path, temp_in.name]
            Popen(args,
                 stdout=DEVNULL,
                 stderr=STDOUT,
                 env={}).wait()
            with open(temp_out.name) as temp_out:
                return temp_out.read()
    except Exception as e:
        raise e
    finally:
        try:
            shutil.rmtree(env_path)  # delete directory
        except OSError as exc:
            if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                raise  # re-raise exception

def convert_type_service(data, type):
    try:
        with tempfile.NamedTemporaryFile(suffix='.odt') as temp_in, tempfile.NamedTemporaryFile(suffix=EXTENSIONS[type]) as temp_out:
            temp_in.write(data)
            temp_in.flush()
            args = [SOFFICE_PYTHON, CONVERTER, temp_in.name, temp_out.name]
            print(' '.join(args))
            Popen(args,
                 stdout=DEVNULL,
                 stderr=STDOUT,
                 env={}).wait()
            return temp_out.read()
    except Exception as e:
        raise e


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.route('/render', methods=['POST'])
def render():
    try:
        data = request.get_json(force=True)
        form_name = os.path.basename(data['formName'])
        values = data['values']
        subdir = None
        if data.get('goodCompaniesTemplate'):
            subdir = 'goodcompanies'
        result = render_odt(form_name, values, subdir=subdir)
        filename = os.path.basename(values.get('filename', data['formName']))
        file_type = values.get('fileType', 'odt')
        if file_type != 'odt' and EXTENSIONS.get(file_type):
            result = convert_type_service(result, file_type)
        return send_file(BytesIO(result),
                         attachment_filename=filename + EXTENSIONS[file_type],
                         as_attachment=True,
                         mimetype=MIMETYPES[file_type])
    except Exception as e:
        print(e)
        raise InvalidUsage(e.message, status_code=500)


@app.route('/convert', methods=['POST'])
def convert():
    try:
        file_type = request.values.get('fileType', 'docx')
        result = request.files['file']
        filename = result.filename
        file = result.read()
        if file_type != 'odt' and EXTENSIONS.get(file_type):
            file = convert_type_service(file, file_type)
        return send_file(BytesIO(file),
                         attachment_filename=os.path.splitext(filename)[0] + EXTENSIONS[file_type],
                         as_attachment=True,
                         mimetype=MIMETYPES[file_type])
    except Exception as e:

        raise InvalidUsage(e.message, status_code=500)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    SOFFICE_PYTHON = '/Applications/LibreOffice.app/Contents/MacOS/python'
    SOFFICE_BIN = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    print('Running on %d' % PORT)
    app.run(port=PORT, debug=True)
