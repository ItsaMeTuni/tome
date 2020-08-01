import uuid
from typing import Optional

import asyncpg  # type: ignore
from starlette.requests import Request

from tome.database import connection, dynamic_update_query
from tome.exceptions import HTTPException
from tome.middleware.auth import requires
from tome.responses import ORJSONResponse
from tome.routing import post, patch, delete, get
from tome.utils import get_json, validate_types_raising


@post("/api/nodes")
@requires("nodes.create")
async def create_node(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, {"parent": Optional[str], "content": Optional[str]})

    parent = None
    if "parent" in json:
        try:
            parent = uuid.UUID(json["parent"])
        except ValueError as e:
            raise HTTPException("invalid ID", 422) from e

    try:
        result = await connection().fetchval(
            "insert into nodes (user_id, parent) values ($1, $2) returning id",
            request.user.id,
            parent,
        )
    except asyncpg.ForeignKeyViolationError as e:
        raise HTTPException("Parent node does not exist", 404) from e

    return ORJSONResponse(result)


@delete("/api/nodes")
@requires("nodes.delete")
async def create_node(request: Request) -> ORJSONResponse:
    try:
        id_ = uuid.UUID(request.query_params.get("id"))
    except (ValueError, TypeError) as e:
        raise HTTPException("invalid ID", 422) from e

    result = await connection().execute("""delete from nodes where id = $1""", id_)
    if result != "DELETE 1":
        raise HTTPException("not found", 404)

    return ORJSONResponse()


_modify_node_query = dynamic_update_query(
    "nodes",
    ["content", "parent"],
    "where id = $1 returinng *",
    1
)


@patch("/api/nodes")
@requires("nodes.modify")
async def modify_node(request: Request) -> ORJSONResponse:
    try:
        id_ = uuid.UUID(request.query_params.get("id"))
    except (ValueError, TypeError) as e:
        raise HTTPException("invalid ID", 422) from e

    json = await get_json(request)
    validate_types_raising(json, {"content": Optional[str], "parent": Optional[str]})

    query = _modify_node_query(json, id_)

    try:
        result = await connection().fetchrow(*query)
    except (TypeError, ValueError) as e:
        raise HTTPException("Invalid ID", 422) from e
    except asyncpg.ForeignKeyViolationError as e:
        raise HTTPException("Parent does not exist", 404) from e

    return ORJSONResponse(result)


@get("/api/nodes")
@requires("nodes.read")
async def get_nodes(request: Request) -> ORJSONResponse:
    try:
        limit = int(request.query_params.get("limit", 50))
    except ValueError as e:
        raise HTTPException("Invalid limit", 422) from e
    if limit > 100:
        raise HTTPException("Limit too large", 422)

    if "all" in request.query_params:
        cursor = await connection().fetch(
            "select * from nodes where user_id = $1 order by id limit $2;",
            request.user.id,
            limit,
        )
        return ORJSONResponse(list(cursor))

    # if parent is not in params, it is none, so it gets the nodes at the root
    id_ = request.query_params.get("parent")
    cursor = await connection().fetch(
        "select * from nodes where user_id = $1 and parent = $2 order by id limit $3;",
        request.user.id,
        id_,
        limit,
    )
    return ORJSONResponse(list(cursor))
