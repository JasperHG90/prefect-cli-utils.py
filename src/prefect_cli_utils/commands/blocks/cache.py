import logging

import typer

from prefect_cli_utils.blocks import PropertyCache

logger = logging.getLogger("prefect_cli_utils.commands.blocks.cache")


cache = typer.Typer(
    help="💼 Configure prefect property cache blocks", no_args_is_help=True
)


@cache.command(
    name="register",
    short_help="💼 Define a cache block used by Funda pipelines to cache the last property seen during a run",
    no_args_is_help=True,
)
def register_cache(
    name: str = typer.Argument(None, help="Name of the prefect block"),
    url: str = typer.Argument(
        None,
        help="Funda URL (without domain and schema) that will be used as a cache for the ETL flow",
    ),
    overwrite: bool = typer.Option(
        default=True, help="If set to true, then any existing block will be overwritten"
    ),
):
    logger.debug("Registering block")
    cache = PropertyCache(url=url)
    cache.save(name=name, overwrite=overwrite)  # type: ignore
    logger.debug("🔥 Finished setting up the property cache infrastructure block")
