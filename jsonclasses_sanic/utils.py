from typing import TypeVar
from inflection import underscore

T = TypeVar('T')

def recursive_snake_keys(json: T) -> T:
    if json is None:
        return None
    elif isinstance(json, list):
        return [recursive_snake_keys(v) for v in json]
    elif isinstance(json, dict):
        return {underscore(k): recursive_snake_keys(v) for k, v in json.items()}
    else:
        return json
