from rich.panel import Panel
from rich import print


def print_error_inline(message: str, postmessage: str = "") -> None:
    """
    Print an error message in red.
    """
    print(f"[bold red]{message}[/bold red] {postmessage}")


def print_message_inline(message: str, postmessage: str = "") -> None:
    """
    Print a message in blue.
    """
    print(f"[bold cyan]{message}[/bold cyan] {postmessage}")
