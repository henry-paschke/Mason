import typer
from masonml.commands import init

app = typer.Typer()

app.command()(init)


if __name__ == "__main__":
    app()
