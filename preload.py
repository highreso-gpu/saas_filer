import os
import subprocess

def preload(_):
    """start Flask server for uploading"""
    flask_path = os.path.join(os.path.abspath("."), "extensions/saas_filer/api/flask_app.py")
    print()
    print("### Start a server for API endpoints for file operations")
    print("#   -> path: '{}'".format(flask_path))
    print()

    #* start background process
    subprocess.Popen(['python3', flask_path])
