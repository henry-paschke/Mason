from masonml.utils.utils import (
    detect_cuda_version,
    is_nvidia_smi_available,
    validate_python_version_format,
)
from typing import Optional
from masonml.commands.formatting import print_error_inline, print_message_inline
import typer, sys
from masonml.utils.conda_utils import create_conda_env, is_conda_installed


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

    create_conda_env(project_name, python_version)
