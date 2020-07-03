import typing

import orjson
from starlette.responses import JSONResponse

__all__ = ["ORJSONResponse"]


class ORJSONResponse(JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content)
