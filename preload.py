from dotenv import load_dotenv
import os
import subprocess


# from extensions.saas_filer.const.load import DATA_DIR
"""
Unable to retrieve command-line arguments due to lifecycle constraints, so retrieving from environment variables.
Checking the consistency in const/load.py for each of them.

https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions
> if extension has preload.py file in its root directory, it is loaded before parsing commandline arg
"""
load_dotenv(verbose=True)
DATA_DIR = os.getenv("DATA_DIR", "/storage/userdata")

def preload(_):
    """start Flask server """
    start_flask()

def start_flask():
    """start Flask server for uploading"""
    flask_path = os.path.join(DATA_DIR, "extensions/saas_filer/api/flask_app.py")
    print()

    if not os.path.exists(flask_path):
        print("### Error: Flask server for file operations does not exist")
        print("#   -> path: '{}'".format(flask_path))
        print()
        return

    print("### Start a Flask server for file operations")
    print("#   -> path: '{}'".format(flask_path))
    print()

    #* start background process
    subprocess.Popen(['python3', flask_path])
