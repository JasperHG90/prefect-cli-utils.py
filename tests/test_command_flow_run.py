# import asyncio
# from unittest import mock

# import pytest
# from typer.testing import CliRunner

# from flow_utils.commands import flow_run

# _FLOW_ID = "hfguhewf546372"

# runner = CliRunner()


# @pytest.mark.asyncio
# @mock.patch("flow_utils.commands.flow_run.get_client")
# async def test_get_flow_info(mock_fn):
#     f = asyncio.Future()
#     f.result = {"flow_id": _FLOW_ID}
#     mock_fn.result.__enter__.result = f
#     flow_run._get_flow_info(_FLOW_ID)
#     mock_fn.assert_called_with()
