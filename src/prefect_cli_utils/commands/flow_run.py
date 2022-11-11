import asyncio
import logging
import time

import httpx
import typer
from fastapi import status
from prefect.client import get_client  # type: ignore
from prefect.client.schemas import FlowRun

logger = logging.getLogger("flow_utils.commands.flow")

flow_run = typer.Typer(
    help="🔍 Trace a flow and exit successfully when flow completes or fail if flow fails.",
    no_args_is_help=True,
)


async def _get_flow_info(id: str) -> FlowRun:
    async with get_client() as client:
        try:
            flow_run = await client.read_flow_run(id)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == status.HTTP_404_NOT_FOUND:
                raise ValueError(f"Flow run {id!r} not found!")
            else:
                raise
    return flow_run


@flow_run.command(
    name="trace",
    short_help="🔍 Trace a prefect deployment run until flow completion or failure",
)
def stop_for_flow_status(
    id: str = typer.Argument(default=None, help="ID of the deployment run"),
    poll_seconds: int = typer.Argument(
        default=None,
        help="Number of seconds between retrying the API to check for flow completion",
    ),
    timeout_in_minutes: int = typer.Argument(
        None, help="Number of minutes after which the program will time out and exit"
    ),
):
    logger.debug(f"Tracing flow with id={id}")
    if (poll_seconds / 60) > timeout_in_minutes:
        raise ValueError("Polling interval cannot exceed timeout condition")
    t_delta = 0
    flow_exited = False
    flow_state: str = "SCHEDULED"
    while (not flow_exited) and ((t_delta / 60) < timeout_in_minutes):
        flow_info = asyncio.run(_get_flow_info(id))
        flow_state = str(flow_info.state.type).split(".")[-1]  # type: ignore
        if flow_state in ["PENDING", "RUNNING", "SCHEDULED"]:
            logger.debug(f"Flow with id={id} is in state '{flow_state}'")
            logger.debug(f"Sleeping for {poll_seconds} seconds ...")
            t_delta += poll_seconds
            time.sleep(poll_seconds)
        else:
            flow_exited = True
    if not flow_exited:  # timeout
        raise TimeoutError(
            f"Timeout expired for flow with id={id} and timeout_in_minutes={timeout_in_minutes}"
        )
    if flow_state in ["CANCELED", "CRASHED", "FAILED"]:
        logger.debug(f"Flow with id={id} failed with state '{flow_state}'")
        if flow_info.state.message.startswith(  # type: ignore
            "Flow run encountered an exception. flow_utils.exceptions.NoResultsException"
        ):
            logger.debug(
                "Exception indicates no new listings available. Exiting gracefully ..."
            )
            return None
        logger.debug(flow_info.json())
        raise ValueError(f"Flow with id={id} failed with state '{flow_state}'")
    if flow_state == "COMPLETED":
        logger.info(f"Flow with id={id} completed successfully. Exiting ...")
