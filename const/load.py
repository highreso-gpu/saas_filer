from dotenv import load_dotenv
import os
import subprocess


def extract_script_args(param: str) -> str:
    """Extracting a parameter from a script for launching the application."""

    try:
        script_path = os.path.join(os.path.abspath("."), "webui-user.sh")
        command = f"grep 'export COMMANDLINE_ARGS' {script_path} | grep -v '#' | sed 's/.*--{param}=\\([^ \"]*\\).*/\\1/' | tr -d '\\n'"
        ret = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"{param}: {ret.stdout}")
        return ret.stdout

    except subprocess.CalledProcessError as cpe:
        # when returncode is not 0
        print(f"returncode: {str(cpe.returncode)}")
        print(f"stderr: {cpe.stderr}")
        print(f"cmd: {cpe.cmd}")
        raise cpe

def compare_parameters(param_first: str, param_second: str) -> None:
    """
    Check if the parameters are the same.
    Due to lifecycle constraints, we need to ensure consistency because some parameters are retrieved from .env in preload.py.
    """
    
    if param_first != param_second:
        raise ValueError(f"Parameters do not match: {param_first} != {param_second}")

"""
Load environment variables from a .env file for development environment.

If necessary, create a .env file in the root directory of this extension.
(Note: This is not necessary for production environment.)
"""
load_dotenv(verbose=True)

SAAS_DOMAIN = os.getenv("SAAS_DOMAIN", "imagegen.highreso.jp")
FLASK_PORT = os.getenv("FLASK_PORT", 55000)

# development
DATA_DIR = os.path.abspath(".")             # Application root
SUB_PATH = ''                               # No need to specify a subpath

if not SAAS_DOMAIN in ["localhost", "127.0.0.1"]:
    # production
    DATA_DIR = extract_script_args('data-dir')  # Path for persistent data
    SUB_PATH = extract_script_args('subpath')   # Subpath for the application

    env_data_dir = os.getenv("DATA_DIR", "/storage/userdata")
    compare_parameters(DATA_DIR, env_data_dir)
