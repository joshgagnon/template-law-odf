from secretary import Renderer
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

try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

logging.basicConfig()

PORT = 5668
SOFFICE_BIN = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

engine = Renderer()
app = Flask(__name__)

MIMETYPES = {
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'odt': 'application/vnd.oasis.opendocument.text',
    'pdf': 'application/pdf'
}

EXTENSIONS = {
    'pdf': '.pdf',
    'odt': '.odt',
    'docx': '.docx'
}


def convert_type(data, type):
    env_path = tempfile.mkdtemp()
    try:
        with tempfile.NamedTemporaryFile(suffix='.odt') as temp_in:
            temp_in.write(data)
            temp_in.flush()
            args = [SOFFICE_BIN, "-env:UserInstallation=file://%s" % env_path, "--headless",
                 "--invisible", "--convert-to", "pdf",  "--outdir", env_path, temp_in.name]
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


@app.route('/render')
def render():
    try:
        data = request.get_json(force=True)
        with open('templates/' + os.path.basename(data['formName']) + '.odt') as template:
            result = engine.render(template, **data)
            filename = os.path.basename(data.get('fileName', data['formName']))
            if data['fileType'] != 'odt':
                result = convert_type(result, data['fileType'])
            return send_file(BytesIO(result),
                             attachment_filename=filename + EXTENSIONS[data['fileType']],
                             as_attachment=True,
                             mimetype=MIMETYPES[data['fileType']])
    except Exception, e:
        print e
        raise InvalidUsage(e.message, status_code=500)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    print 'Running on', PORT
    app.run(port=PORT, debug=True)
