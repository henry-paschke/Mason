import typer
from masonml.utils import print_error_inline, print_message_inline
from masonml.utils.conda_utils import delete_conda_env
from masonml.lockfile.schema import Lock_file, load_lock_file
from pathlib import Path


def delete(
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force delete the environment without confirmation.",
    ),
    remove_lockfile: bool = typer.Option(
        False,
        "--remove-lockfile",
        "-r",
        help="Remove the lockfile after deleting the environment.",
    ),
) -> None:
    """
    Delete the environment in the current folder.
    """
    mason_lock_path = Path.cwd() / "mason-lock.yaml"
    if not mason_lock_path.exists():
        print_error_inline(
            "'mason-lock.yaml' not found, nothing can be deleted.",
            "Please run 'mason init' to initialize a new project.",
        )
        raise typer.Exit(1)

    if not force:
        confirm = input(
            f"Are you sure you want to delete the environment in this folder'? (y/n): "
        )
        if confirm.lower() != "y":
            print("Operation cancelled.")
            raise typer.Exit(0)

    try:
        lock_file = load_lock_file(mason_lock_path)
        # Assuming `delete_conda_env` is a function that deletes the conda environment
        delete_conda_env(lock_file.conda_env_name)
        print_message_inline(
            f"Environment '{lock_file.conda_env_name}' deleted successfully."
        )
    except Exception as e:
        print_error_inline(
            f"Error deleting environment '{lock_file.conda_env_name}': ", e
        )
        raise typer.Exit(1)

    if remove_lockfile:
        try:
            mason_lock_path.unlink()
            print_message_inline("Lockfile removed successfully.")
        except Exception as e:
            print_error_inline("Error removing lockfile: ", e)
            raise typer.Exit(1)
