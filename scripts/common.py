from pathlib import Path
import sys

# Import from parent directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from const.load import SAAS_DOMAIN


def is_development() -> bool:
    """Check if the environment is development or production."""
    return SAAS_DOMAIN in ["localhost", "127.0.0.1"]
