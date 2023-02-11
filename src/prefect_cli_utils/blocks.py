from prefect.blocks.core import Block


class PropertyCache(Block):
    """Used by Funda pipelines to cache the last property seen during a run"""

    url: str
