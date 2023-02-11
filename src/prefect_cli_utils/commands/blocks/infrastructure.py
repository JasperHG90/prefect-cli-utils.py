import logging
import typing

import typer
from prefect.infrastructure.docker import DockerContainer, DockerRegistry

logger = logging.getLogger("prefect_cli_utils.commands.blocks.infrastructure")

infra = typer.Typer(
    help="🏭 Configure prefect infrastructure blocks", no_args_is_help=True
)
docker_registry = typer.Typer(
    help="🔧 Register a prefect infrastructure block for the private docker registry on GCP that is used by the Funda ETL flows.",
    no_args_is_help=True,
)
docker_container = typer.Typer(
    help="📦 Register a prefect infrastructure block for the docker container that is used by the Funda ETL flows.",
    no_args_is_help=True,
)
infra.add_typer(docker_registry, name="docker-registry")
infra.add_typer(docker_container, name="docker-container")


@docker_registry.command(
    name="register",
    short_help="🔧 Define and save a prefect infrastructure block for a docker registry",
)
def register_block_docker_registry(
    name: str = typer.Argument(None, help="Name of the prefect block"),
    registry_url: str = typer.Argument(None, help="URL of the docker registry"),
    username: str = typer.Argument(
        None,
        help="Username for the docker registry",
    ),
    password: str = typer.Argument(
        None,
        help="Password for the docker registry",
    ),
    overwrite: bool = typer.Option(
        True, help="If set to true, then any existing block will be overwritten"
    ),
):
    logger.debug("Registering block")
    registry = DockerRegistry(
        username=username,
        password=password,
        registry_url=registry_url,
    )
    registry.save(name=name, overwrite=overwrite)  # type: ignore
    logger.debug("🔥 Finished setting up docker registry")


@docker_container.command(
    name="register",
    short_help="🔧 Define and save a prefect infrastructure block for a docker container",
)
def register_block_docker_container(
    name: str = typer.Argument(None, help="Name of the prefect block"),
    image: str = typer.Argument(None, help="Name of the docker image"),
    image_pull_policy: str = typer.Argument(
        default="ALWAYS", help="Image pull policy to use. Defaults to 'ALWAYS'."
    ),
    registry_block_name: typing.Optional[str] = typer.Option(
        default=None,
        help="Name of the prefect docker registry block if using a private docker registry",
    ),
    overwrite: bool = typer.Option(
        default=True, help="If set to true, then any existing block will be overwritten"
    ),
):
    logger.debug("Registering block")
    if registry_block_name is not None:
        registry = DockerRegistry.load(registry_block_name)
    else:
        registry = None
    container = DockerContainer(
        image=image,
        image_pull_policy=image_pull_policy,
        image_registry=registry,
    )
    container.save(name=name, overwrite=overwrite)  # type: ignore
    logger.debug("🔥 Finished setting up docker container")
