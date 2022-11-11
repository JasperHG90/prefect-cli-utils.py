from typer.testing import CliRunner

from prefect_cli_utils.cli import app


def test_listings_cli():
    runner = CliRunner()
    result = runner.invoke(app, ["prefect_cli_utils", "/path/to/file.parquet"])
    assert result.exit_code == 0
