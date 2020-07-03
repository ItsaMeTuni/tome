import asgi_lifespan
import httpx
import pytest


@pytest.fixture
async def client():
    """fixture to provide a http AsyncClient on our app"""
    from tome.app import app
    import tome.database

    async with asgi_lifespan.LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            transaction = tome.database.connection().transaction()
            await transaction.start()
            try:
                yield client
            finally:
                await transaction.rollback()


@pytest.fixture
async def db():
    """fixture to provide a database client with a transaction that will be rolled back
    """
    import tome.database

    await tome.database.connect()
    transaction = tome.database.connection().transaction()
    await transaction.start()
    yield tome.database.connection()
    await transaction.rollback()
    await tome.database.disconnect()
