import asyncio
import warnings
from typing import (  # type: ignore
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Coroutine,
    Final,
    Literal,
    Optional,
    Tuple,
    Union,
    get_origin,
    _TypedDictMeta,
)

import orjson
import starlette.requests

from tome.exceptions import HTTPException


class ORJSONCodec:
    """JSON encoder and decoder using orjson.

    Can be used in place of either json.JSONDecoder or json.JSONEncoder.
    """

    def __init__(
        self,
        *,
        orjson_default: Optional[Callable[[Any], Any]] = None,
        orjson_option: Optional[int] = 0,
        **_ignore: Any,
    ):
        self.default = orjson_default
        self.option = orjson_option

    def encode(self, data: Any) -> str:
        return orjson.dumps(data, default=self.default, option=self.option).decode()

    def decode(self, data: str) -> Any:
        return orjson.loads(data)


async def get_json(request: starlette.requests.Request) -> Any:
    """
    return json data from a request, raising appropriate http exceptions if invalid
    :param request: starlette request object
    :return: any valid JSON data
    """
    body = await request.body()
    try:
        return orjson.loads(body)
    except orjson.JSONDecodeError as e:
        raise HTTPException(f"invalid json: {e}", 400)


class TypeWarning(Warning):
    pass


def validate_types(data: Any, type_: Any, /) -> bool:
    """Validate data according to a standard PEP 484 type annotation

    Validates Any, None, Union, Optional, Literal, Tuple, List, Dict, TypedDict, Final,
    str, int, float, bool, bytes, dict, float

    Also, you can pass an __annotations__-style dictionary to be validated.
    For example::

        class Foo:
            x: int
            y: str

        validate_types({"x": 12, "y": "hi"}, Foo.__annotations__)
        validate_types({"x": 12, "y": "hi"}, {"x": int, "y": str})

    This function cannot validate TypeVars.

    :param data: data from JSON
    :param type_: PEP 484 type annotation or type or
    :return: boolean, validation succeeded or not
    """

    if type_ is Any:
        return True
    elif type_ is None or type_ is type(None):  # noqa: E721
        return data is None
    elif origin := get_origin(type_):
        # special PEP 484 types like like Dict (not Dict[x, y] or dict) can just be used
        # with isinstance
        try:
            return isinstance(data, origin)
        except TypeError:
            if origin is Union:
                return any(validate_types(data, t) for t in type_.__args__)
            elif origin is Literal:
                return data in type_.__args__
            elif origin is Final or origin is ClassVar:
                return validate_types(data, type_.__args__[0])
            elif origin is tuple:
                return (
                    isinstance(data, (list, tuple))
                    and len(data) == len(type_.__args__)
                    and all(
                        validate_types(v, type_.__args__[i]) for i, v in enumerate(data)
                    )
                )
            elif origin is list:
                return isinstance(data, list) and all(
                    validate_types(v, type_.__args__[0]) for v in data
                )
            elif origin is dict:
                return (
                    isinstance(data, dict)
                    and all(validate_types(k, type_.__args__[0]) for k in data)
                    and all(validate_types(v, type_.__args__[1]) for v in data.values())
                )
            else:
                raise TypeError(f"cannot validate {type_}")
    # TODO(pxeger): replace with stable/public API -
    #  see https://github.com/python/typing/issues/751
    elif isinstance(type_, _TypedDictMeta):  # type: ignore
        # PEP 589 TypedDict
        return validate_types(data, type_.__annotations__)
    elif isinstance(type_, dict):
        # { name: type } dict
        return (
            isinstance(data, dict)
            and not (type_.keys() - data.keys())
            and all(validate_types(v, type_.get(k)) for k, v in data.items())
        )
    elif isinstance(type_, set):
        return any(validate_types(data, t) for t in type_)
    else:
        if not isinstance(type_, type):
            raise TypeError(f"cannot type-check {type_}")
        elif not issubclass(type_, (str, int, float, bytes, dict, list)):
            # may not be able to reliably type-check non-literals
            warnings.warn(f"naïvely checking type for {type_}", TypeWarning)
        return isinstance(data, type_)


def validate_types_raising(data: Any, type_: Any) -> None:
    """validate types, raising a HTTPException if the types are invalid

    Takes the same parameters as validate_types
    """
    if not validate_types(data, type_):
        raise HTTPException("invalid types", 422)


def simultaneous(
    *functions: Callable[[], Awaitable[Any]]
) -> Tuple[Callable[[], Coroutine[None, None, None]]]:
    """closure, returns a function that can run multiple tasks simultaneously"""

    async def inner() -> None:
        await asyncio.gather(*[function() for function in functions])

    return (inner,)
