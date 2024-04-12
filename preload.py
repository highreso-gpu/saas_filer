import os
import subprocess


def preload(_):
    """start Flask server """
    start_flask()

def start_flask():
    """start Flask server for uploading"""
    flask_path = os.path.join(os.path.abspath("."), "extensions-builtin", "saas_filer/api/flask_app.py")
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
