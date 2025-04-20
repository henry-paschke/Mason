from masonml.utils.utils import (
    detect_cuda_version,
    is_nvidia_smi_available,
    validate_python_version_format,
)
from typing import Optional
from masonml.commands.formatting import print_error_inline, print_message_inline
import typer, sys
from pathlib import Path
from masonml.utils.conda_utils import create_conda_env, is_conda_installed
from masonml.lockfile.schema import (
    Lock_file,
    System_info,
    save_lock_file,
)
import platform


def init(
    project_name: str = typer.Argument(
        ...,
        help="Name of the project to initialize.",
    ),
    cuda_version: Optional[str] = typer.Option(
        None, help="Manually specify CUDA version (e.g. 11.8)"
    ),
    python_version: Optional[str] = typer.Option(
        None, help="Manually specify Python version (e.g. 3.8.0)"
    ),
):
    """
    Initialize a new Mason project.
    This command creates a new conda environment for the project and sets up the necessary files.
    """
    mason_lock_path = Path.cwd() / "mason-lock.yaml"
    os_name = platform.system()
    if os_name == "darwin":
        print_error_inline(
            "'macOS' is not supported!", "Please use 'Linux' or 'Windows' instead."
        )
        raise typer.Exit(1)

    if mason_lock_path.exists():
        print_error_inline(
            "'mason-lock.yaml' already exists, a project is already initialized!",
            "Please remove it before initializing a new project.",
        )
        raise typer.Exit(1)

    if not is_nvidia_smi_available():
        print_error_inline("'nvidia-smi' not found!", "Proceeding without CUDA.")
        if cuda_version is not None:
            print_error_inline("Specified CUDA version will be ignored!")
            cuda_version = None
    else:
        if cuda_version is None:
            version = detect_cuda_version()
            print_message_inline("Detected CUDA version:", version)
            cuda_version = version
        else:
            print_message_inline("Using specified CUDA version:", version)

    if python_version is None:
        major = sys.version_info.major
        minor = sys.version_info.minor
        micro = sys.version_info.micro
        python_version = f"{major}.{minor}.{micro}"
        print_message_inline("Using system Python version:", f"{major}.{minor}.{micro}")
    else:
        if not validate_python_version_format(python_version):
            print_error_inline("Invalid Python version format!", "Use 'X.Y.Z'")
            raise typer.Exit(1)
        print_message_inline("Using specified Python version:", python_version)

        if not is_conda_installed():
            print_error_inline(
                "'conda' not found!", "Conda is required for Mason to function."
            )
            raise typer.Exit(1)

    try:
        create_conda_env(project_name, python_version)
    except ValueError as e:
        print_error_inline(str(e))
        raise typer.Exit(1)

    lockfile = Lock_file(
        system_info=System_info(
            os=os_name,
            cuda_version=cuda_version,
            python_version=[int(i) for i in python_version.split(".")],
        ),
        conda_env_name=project_name,
    )

    save_lock_file(lockfile, mason_lock_path)
    print_message_inline("Mason project initialized successfully!")
