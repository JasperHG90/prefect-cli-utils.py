# read version from installed package
from importlib.metadata import version

__version__ = version("prefect_cli_utils")
