from dotenv import load_dotenv
import os
import subprocess


load_dotenv(verbose=True)
DATA_DIR = os.getenv("DATA_DIR", "/storage/userdata")

def preload(_):
    """start Flask server """
    start_flask()

def start_flask():
    """start Flask server for uploading"""
    #* webui-user.sh 内の COMMANDLINE_ARGS --data-dir で指定したディレクトリの中にある extensions/saas_filer/api/flask_app.py を起動する
    
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
