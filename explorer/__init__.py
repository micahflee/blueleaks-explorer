import click

from .import_data import run as run_import_data
from .server import run as run_server


def init():
    click.echo(click.style("BlueLeaks Explorer", fg="yellow"))
    click.echo("")


@click.group()
def main():
    """Explore all of the data in BlueLeaks"""


@main.command("import", short_help="Import data into sqlite3 databases")
@click.option(
    "--blueleaks-path", required=True, help="Path to extracted BlueLeaks data",
)
def import_data(blueleaks_path):
    init()
    run_import_data(blueleaks_path)


@main.command("server", short_help="Start server")
@click.option(
    "--blueleaks-path", required=True, help="Path to extracted BlueLeaks data",
)
def server(blueleaks_path):
    init()
    run_server(blueleaks_path)
