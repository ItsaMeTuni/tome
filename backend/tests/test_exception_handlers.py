import orjson
import pytest


@pytest.mark.asyncio
async def test_http_exception_handler():
    import tome.exception_handlers
    from tome.exceptions import HTTPException

    exception = HTTPException({"some": ["json", 45]}, 418)
    response = await tome.exception_handlers.handle_http_exception(None, exception)
    assert orjson.loads(response.body) == {"error": {"some": ["json", 45]}}
    assert response.headers["content-type"] == "application/json"
    assert response.status_code == 418
