# type: ignore[attr-defined]

from enum import Enum

import typer
from rich.console import Console

from svaeva_redux import version
from svaeva_redux.example import hello


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="svaeva-redux",
    help="`svaeva-redux` is a Python cli/package",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]svaeva-redux[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    name: str = typer.Option(..., help="Person to greet."),
    color: Color | None = typer.Option(
        None,
        "-c",
        "--color",
        "--colour",
        case_sensitive=False,
        help="Color for print. If not specified then choice will be random.",
    ),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the svaeva-redux package.",
    ),
) -> None:
    """Print a greeting with a giving name."""
    # if color is None:
    #     color = choice(list(Color))

    greeting: str = hello(name)
    print(f"{greeting}")
    # console.print(f"[bold {color}]{greeting}[/]")


if __name__ == "__main__":
    app()
