import typer

app = typer.Typer()

@app.command()
def init(project_name: str):
    typer.echo(f"Initializing project: {project_name}")

if __name__ == "__main__":
    app()