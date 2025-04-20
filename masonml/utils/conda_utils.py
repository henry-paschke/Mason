import subprocess, typer, shutil
from masonml.commands.formatting import print_error_inline, print_message_inline


def create_conda_env(env_name: str, python_version: str) -> None:
    """
    Create a conda environment with the specified name and Python version.
    """
    process = subprocess.Popen(
        ["conda", "create", "-n", env_name, f"python={python_version}", "-y"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    package_error = True
    if stderr:
        for line in stderr:
            if "PackagesNotFoundError" in line:
                package_error = True
            if "python=" in line and package_error:
                raise ValueError(f"Invalid Python version '{python_version}'.")


def is_conda_installed() -> bool:
    """
    Check if conda is installed on the system.
    """
    return shutil.which("conda") is not None


def delete_conda_env(env_name: str) -> None:
    """
    Delete a conda environment with the specified name.
    """
    process = subprocess.Popen(
        ["conda", "env", "remove", "-n", env_name, "--all", "-y"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    if stderr:
        for line in stderr:
            if "EnvironmentNameNotFound" in line:
                raise ValueError(f"Environment '{env_name}' not found.")
