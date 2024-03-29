import os
from pathlib import Path
import sys

from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import from parent directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from const.load import SAAS_DOMAIN, FLASK_PORT, SUB_PATH
import scripts.common as common

app = Flask(__name__)

# CORS settings
# FIXME Requests are allowed even from origins outside the configured set.
allowed_origins = "*" if common.is_development() else [f"{scheme}://{SAAS_DOMAIN}:*" for scheme in ["http", "https"]]
CORS(app, resources={rf"/{SUB_PATH}*": {"origins": allowed_origins}})

@app.route('/upload', methods=['POST'])
def upload_file() -> str:
    """
    [CAUTION] Overwrite request.files in path if already exists.
    
    We assume that the traffic is very low and self-contained within the same host,
    and we do not require advanced features or log management. Therefore, we will
    use werkzeug even in the production environment.
    """
    app.config['UPLOAD_DIR'] = request.form['target_path']

    if 'file' not in request.files:
        return 'Please select a file'

    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
        return 'Upload process completed successfully'
    
    except Exception as e:
        return f"Upload process failed<br>({e})"

if __name__ == '__main__':
    print(" * Allowing origins:", allowed_origins)
    # Production environment will result in a 502 Bad Gateway error in nginx if not exposed externally.
    app.run(host='0.0.0.0', port=FLASK_PORT)
