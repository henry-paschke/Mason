import subprocess, typer, shutil
from masonml.commands.formatting import print_error_inline, print_message_inline


def create_conda_env(env_name: str, python_version: str) -> None:
    """
    Create a conda environment with the specified name and Python version.
    """
    try:
        process = subprocess.Popen(
            ["conda", "create", "-n", env_name, f"python={python_version}", "-y"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.wait()
        package_error = True
        for line in process.stderr:
            if "PackagesNotFoundError" in line:
                package_error = True
            if "python=" in line and package_error:
                print_error_inline("Invalid python version:", python_version)
                raise typer.Exit(1)

        print_message_inline(f"Conda environment '{env_name}' created successfully!")
    except subprocess.CalledProcessError as e:
        print_error_inline(f"Error creating conda environment: {e.stderr.decode()}")
        raise e


def is_conda_installed() -> bool:
    """
    Check if conda is installed on the system.
    """
    return shutil.which("conda") is not None
