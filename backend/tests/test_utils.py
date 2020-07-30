import sys
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Final,
    List,
    Literal,
    Optional,
    Tuple,
    TypedDict,
    Union,
)

import orjson
import pytest

from tome.exceptions import HTTPException


def _test_http_exception_code(status_code, /):
    def inner():
        _, exc, _ = sys.exc_info()
        assert exc.status_code == status_code

    return inner


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_get_json() -> None:
    import tome.utils

    class FakeRequest:
        def __init__(self, body: bytes) -> None:
            self._body = body

        async def body(self) -> bytes:
            return self._body

    fake_data = {"some": "result", "unicode": "☭"}
    assert fake_data == await tome.utils.get_json(FakeRequest(orjson.dumps(fake_data)))

    with pytest.raises(HTTPException) as exc_info:
        bad_json = orjson.dumps(fake_data)[:-2]
        await tome.utils.get_json(FakeRequest(bad_json))

    assert exc_info.value.status_code == 400


def test_validate_types() -> None:
    import tome.utils

    assert tome.utils.validate_types(43, int)
    assert not tome.utils.validate_types("foo", int)
    assert not tome.utils.validate_types(b"\0", int)
    assert not tome.utils.validate_types(b"\0", int)
    assert not tome.utils.validate_types(b"foo", str)
    assert not tome.utils.validate_types("foo", bytes)
    assert not tome.utils.validate_types(None, int)
    assert not tome.utils.validate_types(43, float)
    assert not tome.utils.validate_types(43.0, int)
    assert not tome.utils.validate_types(1, bool)
    assert tome.utils.validate_types(True, bool)
    assert tome.utils.validate_types(None, None)
    assert not tome.utils.validate_types(43, None)
    assert not tome.utils.validate_types(43, None)
    assert not tome.utils.validate_types(43, {"foo": int})
    assert tome.utils.validate_types({"foo": 43}, {"foo": int})
    assert not tome.utils.validate_types({"foo": 43, "extra": False}, {"foo": int})
    assert tome.utils.validate_types(
        {"foo": 43, "bar": "bar"}, {"foo": int, "bar": Optional[str]}
    )
    assert tome.utils.validate_types(
        {"foo": 43, "bar": None}, {"foo": int, "bar": Optional[str]}
    )
    assert tome.utils.validate_types({"foo": 43}, {"foo": int, "bar": Optional[str]})
    assert tome.utils.validate_types(43, Optional[int])
    assert tome.utils.validate_types(43, Final[int])
    assert tome.utils.validate_types(43, ClassVar[int])
    assert tome.utils.validate_types(None, Optional[int])
    assert tome.utils.validate_types("43", Union[int, str])
    assert tome.utils.validate_types(43, Union[int, str])
    assert not tome.utils.validate_types(None, Union[int, str])
    assert tome.utils.validate_types("43", {int, str})
    assert tome.utils.validate_types(43, {int, str})
    assert not tome.utils.validate_types(None, {int, str})
    assert tome.utils.validate_types(object(), Any)
    assert tome.utils.validate_types((43, "foo"), Tuple[int, str])
    assert tome.utils.validate_types([43, "foo"], Tuple[int, str])
    assert not tome.utils.validate_types((43, "foo", "extra"), Tuple[int, str])
    assert tome.utils.validate_types([43, 34], List[int])
    assert not tome.utils.validate_types("foo", List[str])
    assert not tome.utils.validate_types([43, "foo"], List[int])
    assert tome.utils.validate_types(43, Literal[43])
    assert not tome.utils.validate_types(67, Literal[43])
    assert tome.utils.validate_types("foo", Literal[43, "foo"])
    assert not tome.utils.validate_types(67, Literal[43, "foo"])
    assert tome.utils.validate_types({43: "foo"}, Dict[int, str])
    assert not tome.utils.validate_types(43, Dict[int, str])
    assert not tome.utils.validate_types({43: False}, Dict[int, str])
    assert not tome.utils.validate_types({43: "foo", 67: False}, Dict[int, str])
    assert tome.utils.validate_types({}, Dict)
    assert not tome.utils.validate_types("foo", Dict)

    class FooTypedDict(TypedDict):
        foo: int
        bar: str

    assert tome.utils.validate_types({"foo": 43, "bar": "43"}, FooTypedDict)

    with pytest.raises(TypeError):
        tome.utils.validate_types(43, object())

    with pytest.raises(TypeError):
        tome.utils.validate_types(43, Callable[[int], str])

    class Arbitrary:
        pass

    with pytest.warns(Warning):
        assert tome.utils.validate_types(Arbitrary(), Arbitrary)
    with pytest.warns(Warning):
        assert not tome.utils.validate_types(43, Arbitrary)


def test_validate_types_raising():
    import tome.utils

    with pytest.raises(HTTPException) as exc_info:
        tome.utils.validate_types_raising(43, str)

    assert exc_info.value.status_code == 422

    tome.utils.validate_types_raising(43, int)


def test_orjson_codec():
    import tome.utils

    codec = tome.utils.ORJSONCodec()

    assert isinstance(codec.encode({"foo": 43}), str)
    assert codec.decode(codec.encode({"foo": 43})) == {"foo": 43}
