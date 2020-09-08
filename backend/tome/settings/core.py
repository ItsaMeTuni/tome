import os
from typing import Any

_PREFIX = "TOME_"


def get(name: str, default: Any = ..., prefix: str = _PREFIX) -> Any:
    v = os.getenv(prefix + name.upper())
    if not v and default is ...:
        raise Exception(
            f"missing required environment variable {prefix + name.upper()}"
        )
    return v or default


def as_bool(string: str) -> bool:
    return (
        string.lower().startswith("y")
        or string.lower().startswith("t")
        or string.lower().startswith("1")
    )
