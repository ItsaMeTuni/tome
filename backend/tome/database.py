import uuid
from typing import Any, Callable, Iterable

import asyncpg  # type: ignore

from tome import settings
from tome.exceptions import HTTPException

_connection: asyncpg.Connection = None


def connection() -> asyncpg.Connection:
    return _connection


def _uuid_coerce(value: Any) -> bytes:
    # TODO(pxeger) PEP 622
    if isinstance(value, str):
        return uuid.UUID(value).bytes
    elif isinstance(value, bytes):
        return value
    elif isinstance(value, uuid.UUID):
        return value.bytes
    elif isinstance(value, int):
        return uuid.UUID(int=value).bytes
    else:
        raise TypeError(f"cannot coerce object of type {type(value)} to a UUID")


async def connect() -> None:
    global _connection
    if not _connection or not _connection.is_closed():
        _connection = await asyncpg.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
        )
        await _connection.set_type_codec(
            "uuid",
            encoder=_uuid_coerce,
            decoder=lambda u: uuid.UUID(bytes=u),
            schema="pg_catalog",
            format="binary",
        )


async def disconnect() -> None:
    global _connection
    if connection:
        await _connection.close()
        _connection = None


def dynamic_update_query(
    table_name: str,
    columns: Iterable[str],
    extra_clause: str = "",
    placeholders: int = 0,
) -> Callable:
    """closure. creates a dynamic SQL update query using values provided

    for example:
        update_user = dynamic_update_query("users", "id", "name", "email", "id = 345")
        data = {
            "name": "hello",
            "email": None
        }
        query = update_user(data)
        await db.execute(*query)

    Same as `update users set id = id, name = 'hello', email = NULL where id = 345`


    table_name, columns, and where must be sanitised!!"""

    # format-ception
    update = ", ".join(map("{} = {{}}".format, columns))
    template = "update {} set {} {}".format(table_name, update, extra_clause)
    # template is now something like "update users set id = {}, name = {}, email = {}
    #   where id = 345"

    # it is then formatted in the closure to be something like this:
    # "update users set id = id, name = $1, email = $2 where id = 345"

    def inner(data: dict, *extra: Any) -> Iterable[Any]:
        nonlocal placeholders

        # if there are any provided keys that don't exist as columns
        if data.keys() - columns:
            raise HTTPException("invalid types", 422)

        format_args = []
        values = []
        for column in columns:
            if column in data:
                # format with a postgresql placeholder
                format_args.append("$" + str(placeholders))
                values.append(data[column])
                placeholders += 1
            else:
                # format with the column name, to keep the existing stored value
                format_args.append(column)

        return template.format(*format_args), *extra, *values

    return inner
