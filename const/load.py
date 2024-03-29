from dotenv import load_dotenv
import os
import subprocess


def extract_subpath() -> str:
    """Get the subpath because these parameters cannot be obtained with os.getenv() in the shell."""

    try:
        script_path = os.path.join(os.path.abspath("."), "webui-user.sh")
        command = f"grep 'export COMMANDLINE_ARGS' {script_path} | grep -v '#' | sed 's/.*--subpath=\\([^ \"]*\\).*/\\1/'"
        ret = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"subpath: {ret.stdout}")
        return ret.stdout

    except subprocess.CalledProcessError as cpe:
        # when returncode is not 0
        print(f"returncode: {str(cpe.returncode)}")
        print(f"stderr: {cpe.stderr}")
        print(f"cmd: {cpe.cmd}")
        raise cpe

"""
Load environment variables from a .env file for development environment.

If necessary, create a .env file in the root directory of this extension.
(Note: This is not necessary for production environment.)
"""
load_dotenv(verbose=True)

SAAS_DOMAIN = os.getenv("SAAS_DOMAIN", "imagegen.highreso.jp")
FLASK_PORT = os.getenv("FLASK_PORT", 55000)
# Path for extensions
DATA_DIR = os.getenv("DATA_DIR", "/storage/userdata")
# if development environment return empty string 
SUB_PATH = '' if SAAS_DOMAIN in ["localhost", "127.0.0.1"] else extract_subpath()