import json
import pathlib as plb
import tempfile
from unittest import mock

from typer.testing import CliRunner

from prefect_cli_utils.commands.blocks import credentials, infrastructure

runner = CliRunner()


@mock.patch("prefect_cli_utils.commands.blocks.credentials.GcpCredentials")
def test_register_credentials(mock_cls):
    with tempfile.TemporaryDirectory() as tmpdir:
        credentials_info = {"credentials": "this"}
        path_to_credentials = plb.Path(tmpdir) / "credentials.json"
        with path_to_credentials.open("w") as outFile:
            json.dump(credentials_info, outFile)
        cli_out = runner.invoke(
            credentials.gcp_credentials,
            ["my_credentials", str(path_to_credentials), "my-proj-id", "--overwrite"],
        )
    assert cli_out.exit_code == 0
    mock_cls.assert_called_with(
        project="my-proj-id", service_account_info=json.dumps(credentials_info)
    )
    mock_cls.return_value.save.assert_called_with(name="my_credentials", overwrite=True)


@mock.patch("prefect_cli_utils.commands.blocks.infrastructure.DockerRegistry")
def test_register_docker_registry(mock_cls):
    cli_out = runner.invoke(
        infrastructure.docker_registry,
        ["this-registry-name", "my-registry-url.com", "myuser", "mypwd", "--overwrite"],
    )
    assert cli_out.exit_code == 0
    mock_cls.assert_called_with(
        username="myuser",
        password="mypwd",
        registry_url="my-registry-url.com",
    )
    mock_cls.return_value.save.assert_called_with(
        name="this-registry-name", overwrite=True
    )


@mock.patch("prefect_cli_utils.commands.blocks.infrastructure.DockerContainer")
@mock.patch("prefect_cli_utils.commands.blocks.infrastructure.DockerRegistry")
def test_register_docker_container(mock_registry, mock_container):
    cli_out = runner.invoke(
        infrastructure.docker_container,
        [
            "this-container-name",
            "myimage:mytag",
            "--image-pull-policy",
            "ALWAYS",
            "--registry-block-name",
            "this-registry-name",
            "--overwrite",
        ],
    )
    assert cli_out.exit_code == 0
    mock_registry.load.assert_called_with("this-registry-name")
    mock_container.assert_called_with(
        image="myimage:mytag",
        image_pull_policy="ALWAYS",
        image_registry=mock_registry.load.return_value,
    )
    mock_container.return_value.save.assert_called_with(
        name="this-container-name", overwrite=True
    )
