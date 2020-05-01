from typing import Dict
from typing import Any 
from functools import lru_cache
from urllib.parse import urlencode
import os


@lru_cache(maxsize=1)
def get_base_uri():
    """Retrieves base uri based on environment so it will be easier to use different uris on dev
    and prod
    """
    return os.environ.get('BASE_WEB_URI')


@lru_cache(maxsize=10)
def build_full_uri(path: str, query_params: Dict[str, Any] = None) -> str:
    """Build a uri to make it easier to build redirects/callbacks"""
    full_path = get_base_uri() + path
    if query_params:
        return full_path + '?' + urlencode(query_params)
    return full_path 
