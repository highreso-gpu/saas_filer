from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
import os
import werkzeug

"""
Load environment variables from a .env file.

If necessary, create a .env file in the root directory of either the 'saas_filer' or 'stable-diffusion-webui' projects.
(Note: This is usually not necessary.)
"""
load_dotenv(verbose=True)

HOST_DOMAIN = os.getenv("HOST_DOMAIN", "imagegen.highreso.jp")
GRADIO_PORT = os.getenv("GRADIO_PORT", 7860)
FLASK_PORT = os.getenv("API_FILER_PORT", 55000)

app = Flask(__name__)

# CORS settings
allowed_origins = [f"{scheme}://{HOST_DOMAIN}:{GRADIO_PORT}" for scheme in ["http", "https"]]
CORS(app, resources={r"/*": {"origins": allowed_origins}})

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
        filename = werkzeug.utils.secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
        return 'Upload process completed successfully'
    
    except Exception as e:
        return f"Upload process failed<br>({e})"

if __name__ == '__main__':
    print(" * Allowing origins:", allowed_origins)
    app.run(port=FLASK_PORT)

