
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
            print args
            Popen(args,
                 stdout=DEVNULL,
                 stderr=STDOUT,
                 env={}).wait()
            with open(os.path.join(env_path, '%s.%s' % (os.path.basename(temp_in.name)[:-4], type))) as temp_out:
                return temp_out.read()
    except Exception, e:
        raise e
    finally:
        try:
            shutil.rmtree(env_path)  # delete directory
        except OSError as exc:
            if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                raise  # re-raise exception


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
        result = render_odt(form_name, values)
        filename = os.path.basename(values.get('filename', data['formName']))
        file_type = values.get('fileType', 'odt')
        if file_type != 'odt' and EXTENSIONS.get(file_type):
            result = convert_type(result, file_type)
        return send_file(BytesIO(result),
                         attachment_filename=filename + EXTENSIONS[file_type],
                         as_attachment=True,
                         mimetype=MIMETYPES[file_type])
    except Exception, e:
        print e
        raise InvalidUsage(e.message, status_code=500)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    SOFFICE_BIN = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    print 'Running on', PORT
    app.run(port=PORT, debug=True)
