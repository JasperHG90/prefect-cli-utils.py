import hashlib


def hash_url(url: str) -> str:
    """Return the MD5 hash of a URL

    Parameters
    ----------
    url : str
        URL that uniquely identifies a URL

    Returns
    -------
    str
        MD5 hash of the input
    """
    return hashlib.md5(url.encode("utf-8")).hexdigest()
