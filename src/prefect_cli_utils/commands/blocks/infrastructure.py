import logging
import typing

import typer
from prefect.infrastructure.docker import DockerContainer, DockerRegistry
from prefect.infrastructure.kubernetes import KubernetesJob

logger = logging.getLogger("prefect_cli_utils.commands.blocks.infrastructure")

infra = typer.Typer(
    help="🏭 Configure prefect infrastructure blocks", no_args_is_help=True
)
docker_registry = typer.Typer(
    help="🔧 Register a prefect infrastructure block for a docker registry.",
    no_args_is_help=True,
)
docker_container = typer.Typer(
    help="📦 Register a prefect infrastructure block for a docker container.",
    no_args_is_help=True,
)
kubernetes_job = typer.Typer(
    help="☸ Register a prefect infrastructure block for a Kubernetes Job",
    no_args_is_help=True,
)
infra.add_typer(docker_registry, name="docker-registry")
infra.add_typer(docker_container, name="docker-container")
infra.add_typer(kubernetes_job, name="kubernetes-job")


@docker_registry.command(
    name="register",
    short_help="🔧 Define and save a prefect infrastructure block for a docker registry",
    no_args_is_help=True,
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
    no_args_is_help=True,
)
def register_block_docker_container(
    name: str = typer.Argument(None, help="Name of the prefect block"),
    image: str = typer.Argument(None, help="Name of the docker image"),
    image_pull_policy: str = typer.Option(
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


@kubernetes_job.command(
    name="register",
    short_help="☸ Register a prefect infrastructure block for a Kubernetes Job",
    no_args_is_help=True,
)
def register_kubernetes_job(
    name: str = typer.Argument(None, help="Name of the prefect block"),
    image: str = typer.Argument(
        None, help="Name of the docker image used for the Kubernetes job"
    ),
    image_pull_policy: str = typer.Option(
        default="Always", help="Image pull policy to use. Defaults to 'Always'."
    ),
    namespace: typing.Optional[str] = typer.Option(
        default="default",
        help="Namespace in which the job runs. Defaults to 'default'.",
    ),
    service_account_name: typing.Optional[str] = typer.Option(
        default="default",
        help="Service account used by the Kubernetes Job. Defaults to 'default'.",
    ),
    job_watch_timeout_seconds: int = typer.Option(
        default=180,
        help="Number of seconds to watch for job creation before timing out (defaults to 180).",
    ),
    pod_watch_timeout_seconds: int = typer.Option(
        default=180,
        help="Number of seconds to watch for pod creation before timing out (default 180).",
    ),
    finished_job_ttl: typing.Optional[int] = typer.Option(
        default=None,
        help="The number of seconds to retain jobs after completion. If set, finished jobs will be cleaned up by Kubernetes after the given delay. If None (default), jobs will need to be manually removed.",
    ),
    overwrite: bool = typer.Option(
        default=True, help="If set to true, then any existing block will be overwritten"
    ),
):
    logger.debug("Registering block")
    job = KubernetesJob(
        image=image,
        # job=KubernetesJob.job_from_file("./k8s_flow_run_job_manifest.yaml"),
        image_pull_policy=image_pull_policy,
        namespace=namespace,
        service_account_name=service_account_name,
        job_watch_timeout_seconds=job_watch_timeout_seconds,
        pod_watch_timeout_seconds=pod_watch_timeout_seconds,
        finished_job_ttl=finished_job_ttl,
    )
    job.save(name=name, overwrite=overwrite)  # type: ignore
    logger.debug("🔥 Finished setting up docker container")
