import json
import os
from datetime import datetime, timedelta, timezone

from odpt2jre.intermediate_components.output_dict import TrainInformationDict

from . import convert
import odpttraininfo as odpt

_JST = timezone(timedelta(hours=+9), 'JST')

_cache_dir = os.path.join("./__jrecache__/")


def set_cache_dir(dir: str) -> None:
    """Set directory to save cache.
    If dir is not exist, make directories recursively.
    """

    os.makedirs(dir, exist_ok=True)
    if os.path.isdir(dir):
        global _cache_dir
        _cache_dir = dir
    else:
        raise ValueError("Not a directory or failed to make directory.")

def _build_cache_path() -> str:
    return os.path.join( _cache_dir, "JRE.json" )

def _load(expire_second: int = 40) -> list[TrainInformationDict] | None:
    cache_path = _build_cache_path()

    try:
        cache_age = datetime.now(_JST) - datetime.fromtimestamp(os.path.getmtime(cache_path), _JST)
    except FileNotFoundError:
        return None

    if cache_age > timedelta(seconds=expire_second):
        return None

    try:
        with open(cache_path, encoding='utf-8') as loadedCacheJSON:
            return json.load(loadedCacheJSON)
    except FileNotFoundError:
        return None

def _set() -> list[TrainInformationDict]:

    get_info = odpt.fetch_info()

    cache_path = _build_cache_path()

    os.makedirs(_cache_dir, exist_ok=True)

    jre_list:list[TrainInformationDict] = [ info.to_dict() for info in convert.from_odpt_list(get_info) ]

    with open(cache_path, "w", encoding='utf-8') as saveCacheJSON:
        saveCacheJSON.write(json.dumps(jre_list,ensure_ascii=False))

    return jre_list

def refresh_cache() -> None:
    """Refresh caches which is older than 40sec.
    If Failed to download information, it tries to download up to 4 times.
    """

    odpt.refresh_cache()
    _set()

def fetch_info(only_abnormal:bool = False) -> list[TrainInformationDict]:

    result = None

    cache = _load(expire_second=80)
    if cache != None:
        result = cache

    if not result:
        result = _set()

    if only_abnormal:
        return [single for single in result if single["infoStatus"]["id"]!="NORMAL"]
    else:
        return result