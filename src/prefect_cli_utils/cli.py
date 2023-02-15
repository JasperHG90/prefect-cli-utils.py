import logging

import typer

from prefect_cli_utils import __version__
from prefect_cli_utils.commands import flow_run
from prefect_cli_utils.commands.blocks import cache, credentials, infrastructure

logger = logging.getLogger("prefect_cli_utils")
handler = logging.StreamHandler()
format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Silence these loggers
logger_hpack = logging.getLogger("hpack")
logger_httpx = logging.getLogger("httpx")
logger_asyncio = logging.getLogger("asyncio")
logger_hpack.setLevel(logging.ERROR)
logger_httpx.setLevel(logging.ERROR)
logger_asyncio.setLevel(logging.ERROR)

app = typer.Typer(
    help="🧰 Prefect utility CLI functions that can be used to register required infrastructure to run flows.",
    no_args_is_help=True,
)
app.add_typer(infrastructure.infra, name="infrastructure")
app.add_typer(credentials.credentials, name="credentials")
app.add_typer(flow_run.flow_run, name="flow-run")
app.add_typer(cache.cache, name="cache")


@app.command(
    short_help="📌 Displays the current version number of the prefect-cli-utils library"
)
def version():
    print(__version__)


@app.callback()
def main(trace: bool = False):
    if trace:
        logger.setLevel(logging.DEBUG)


def entrypoint():
    app()
