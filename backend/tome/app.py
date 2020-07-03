from starlette.applications import Starlette
from starlette.middleware import Middleware

from tome import database, email
from tome.exception_handlers import handle_http_exception
from tome.exceptions import HTTPException
from tome.middleware.auth import AuthenticationMiddleware
from tome.middleware.request_context import RequestContextMiddleware
from tome.routes import routes
from tome.routing import index

app = Starlette(
    routes=[index, *routes],
    exception_handlers={HTTPException: handle_http_exception},
    middleware=[
        Middleware(RequestContextMiddleware),
        Middleware(AuthenticationMiddleware),
    ],
    on_startup=[database.connect, email.connect],
    on_shutdown=[database.disconnect, email.disconnect],
)
