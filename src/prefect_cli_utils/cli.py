import logging

import typer

from prefect_cli_utils import __version__
from prefect_cli_utils.commands import config
from prefect_cli_utils.steps.example import nchar

logger = logging.getLogger("prefect_cli_utils")
handler = logging.StreamHandler()
format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


app = typer.Typer(
    help="🧰 Example CLI for prefect_cli_utils",
    no_args_is_help=True,
)
app.add_typer(config.config, name="config")


@app.callback()
def main(trace: bool = False):
    if trace:
        logger.setLevel(logging.DEBUG)


@app.command(
    short_help="📌 Displays the current version number of the prefect_cli_utils library"
)
def version():
    print(__version__)


@app.command(
    name="prefect_cli_utils",
    short_help="Prints the number of characters in the input string",
)
def pipeline(input_file: str = typer.Argument(help="Path to input file", default=None)):
    logger.info("Starting pipeline ...")
    logger.debug(f"Ingesting file {input_file}")
    result = nchar(input_file)
    logger.debug(f"File path has {result} characters")
    logger.info("Finished pipeline ...")


def entrypoint():
    app()
