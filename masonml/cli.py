import typer
from masonml.commands import init, delete

app = typer.Typer()


app.command()(init)
app.command()(delete)
