import click

from .import_data import run as run_import_data
from .server import run as run_server
from .structure import run as run_structure


def init():
    click.echo(click.style("BlueLeaks Explorer", fg="yellow"))
    click.echo("")


@click.group()
def main():
    """Explore all of the data in BlueLeaks"""


@main.command("import", short_help="Import data into sqlite3 databases")
def import_data():
    init()
    run_import_data()


@main.command("server", short_help="Start server")
def server():
    init()
    run_server()


@main.command(
    "structure", short_help="Build default structures based on data",
)
def structure():
    run_structure()
