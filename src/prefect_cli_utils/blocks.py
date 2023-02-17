from prefect.blocks.core import Block
from pydantic import SecretStr


class PropertyCache(Block):
    """Used by Funda pipelines to cache the last property seen during a run"""

    url: str


class GcpHmacCredentials(Block):
    """Used to store HMAC S3-compatible credentials"""

    access_key_id: SecretStr
    secret_access_key: SecretStr
