import pytest
from aio_straico import AsyncStraicoClient

@pytest.mark.asyncio
async def test_async_client_initialization():
    client = AsyncStraicoClient()
    assert client is not None
