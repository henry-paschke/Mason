from masonml.commands.utils import detect_cuda_version, is_nvidia_smi_available
from typing import Optional
from rich.panel import Panel
from rich import print
import typer


def init(
    cuda_version: Optional[str] = typer.Option(
        None, help="Manually specify CUDA version (e.g. 11.8)"
    )
):
    if not is_nvidia_smi_available():
        print("[bold red]⚠️ 'nvidia-smi' not found![/bold red] Proceeding without CUDA.")
        if cuda_version is not None:
            print("[bold red]⚠️ Specified CUDA version will be ignored![/bold red]")
            cuda_version = None
    else:
        if cuda_version is None:
            version = detect_cuda_version()
            print(
                f"[bold cyan]Detected CUDA version:[/bold cyan] [green]{version}[/green]",
            )
            cuda_version = version
        else:
            print(
                f"[bold cyan]Using specified CUDA version:[/bold cyan] [green]{cuda_version}[/green]"
            )
