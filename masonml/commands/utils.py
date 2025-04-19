import subprocess
import re
import shutil
from rich import print


def is_nvidia_smi_available() -> bool:
    """
    Check if nvidia-smi is available on the system.
    """
    return shutil.which("nvidia-smi") is not None


def detect_cuda_version():
    """
    Detect if CUDA is available and return the CUDA version.
    """
    output = subprocess.check_output(["nvidia-smi"]).decode()
    match = re.search(r"CUDA Version: (\d+\.\d+)", output.stdout)
    if match:
        return match.group(1)
    else:
        raise ValueError("CUDA version not found in nvidia-smi output")
