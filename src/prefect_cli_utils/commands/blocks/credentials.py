import json
import logging
import pathlib as plb

import typer
from prefect_gcp.credentials import GcpCredentials

logger = logging.getLogger("prefect_cli_utils.commands.blocks.credentials")

credentials = typer.Typer(
    help="🔐 Register prefect credentials block that is used by the Funda ETL flows.",
    no_args_is_help=True,
)


@credentials.command(
    name="register",
    short_help="🔐 Define and save a prefect storage block for GCP credentials",
    help="""This command defines and saves a prefect storage block for GCP credentials.
    Note that you need to have executed `prefect register block -m prefect_gcp.credentials` before
    you can register a block. See <https://docs.prefect.io/concepts/blocks/#registering-blocks-for-use-in-the-prefect-ui>.""",
)
def register_block_credentials(
    name: str = typer.Argument(None, help="Name of the prefect block"),
    credentials_file_path: str = typer.Argument(
        default=None, help="Location of your GCP credentials file"
    ),
    project_id: str = typer.Argument(default=None, help="GCP project id"),
    overwrite: bool = typer.Option(
        default=True, help="If set to true, then any existing block will be overwritten"
    ),
):
    logger.debug("Registering block")
    _credentials_file_path: plb.Path = plb.Path(credentials_file_path).absolute()
    if not _credentials_file_path.exists():
        raise FileNotFoundError(
            f"GCP credentials file not found at '{credentials_file_path}'"
        )
    with _credentials_file_path.open("r") as inFile:
        f = json.load(inFile)
    block = GcpCredentials(project=project_id, service_account_info=json.dumps(f))
    block.save(name=name, overwrite=overwrite)
    logger.debug("🔥 Finished setting up credentials block")
