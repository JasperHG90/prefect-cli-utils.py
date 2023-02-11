from prefect import task

from .utils import hash_url


@task(
    name="Apply MD5 hash",
    description="This task applies the MD5 hashing algorithm to a string input",
)
def md5_hash(x: str) -> str:
    return hash_url(x)
