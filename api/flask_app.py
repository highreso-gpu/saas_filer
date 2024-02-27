from flask import Flask, request
from flask_cors import CORS
import os
import werkzeug

app = Flask(__name__)

# CORS settings
gradio_host = "127.0.0.1:7860"
allowed_origins = [f"{scheme}://{gradio_host}" for scheme in ["http", "https"]]
CORS(app, resources={r"/*": {"origins": allowed_origins}})

@app.route('/upload', methods=['POST'])
def upload_file() -> str:
    """[CAUTION] Overwrite request.files in path if already exists"""
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
    app.run(port=55000)

