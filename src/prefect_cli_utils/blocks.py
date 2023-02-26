from prefect.blocks.core import Block
from pydantic import SecretStr


class PropertyCache(Block):
    """Used by Funda pipelines to cache the last property seen during a run"""

    _block_type_name = "Funda listing cache"

    url: str


class GcpHmacCredentials(Block):
    """Used to store HMAC S3-compatible credentials"""

    # _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/4CD4wwbiIKPkZDt4U3TEuW/c112fe85653da054b6d5334ef662bec4/gcp.png?h=250"  # noqa
    # _block_type_name = "GCP HMAC Credentials"

    access_key_id: SecretStr
    secret_access_key: SecretStr
