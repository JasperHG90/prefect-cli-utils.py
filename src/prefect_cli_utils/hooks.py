import datetime
import typing

import pendulum
from prefect.cli.deployment import get_deployment
from prefect.client import get_client  # type: ignore
from prefect.settings import PREFECT_UI_URL
from prefect.states import Scheduled


async def trigger_deployment(
    deployment_name: str, parameters: typing.Optional[dict] = None
) -> typing.Dict[str, str]:
    """Trigger a prefect deployment flow run

    Parameters
    ----------
    deployment_name : str
        name of the deployment, as '<flow_name>/<deployment_name>'
    """
    async with get_client() as client:
        deployment = await get_deployment(
            client, name=deployment_name, deployment_id=None
        )
        scheduled_start_time = pendulum.instance(
            datetime.datetime.now(), tz="Europe/Amsterdam"
        )
        flow_run = await client.create_flow_run_from_deployment(
            deployment.id,
            parameters=parameters if parameters is not None else {},
            state=Scheduled(scheduled_time=scheduled_start_time),
        )
        run_url = f"{PREFECT_UI_URL.value()}/flow-runs/flow-run/{flow_run.id}"
    return {"flow_run_url": run_url, "flow_run_id": flow_run.id}
