import pytest


@pytest.fixture(scope="function")
async def client(app, aiohttp_client):
    """Test client."""
    client = await aiohttp_client(app)

    return client
