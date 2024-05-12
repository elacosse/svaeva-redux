# type: ignore[attr-defined]


import dotenv
import typer
from rich.console import Console

from svaeva_redux import version as ver
from svaeva_redux.schemas.utils import initialize_redis

app = typer.Typer(
    name="svaeva-redux",
    help="`svaeva-redux` is a Python cli/package",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        raise typer.Exit()


@app.command(name="initialize-db")
def initialize_db() -> None:
    console.print("Initializing redis...")
    initialize_redis()


@app.command()
def version() -> None:
    """Print the version of the package."""
    console.print(f"[yellow]svaeva-redux[/] version: [bold blue]{ver}[/]")


if __name__ == "__main__":
    dotenv.load_dotenv(override=True)
    app()
