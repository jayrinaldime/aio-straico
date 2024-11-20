import pytest
from aio_straico import AsyncStraicoClient
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_async_client_initialization():
    client = AsyncStraicoClient()
    assert client is not None

@pytest.mark.asyncio
async def test_async_client_initialization_with_custom_params():
    client = AsyncStraicoClient(api_key="test_key", base_url="http://test.url")
    assert client.api_key == "test_key"
    assert client.base_url == "http://test.url"

@pytest.mark.asyncio
@patch('aio_straico.AsyncStraicoClient.some_async_method')
async def test_async_client_method_call(mock_method):
    client = AsyncStraicoClient()
    mock_method.return_value = "mocked response"
    response = await client.some_async_method()
    assert response == "mocked response"
    mock_method.assert_called_once()

@pytest.mark.asyncio
async def test_async_client_error_handling():
    client = AsyncStraicoClient()
    with pytest.raises(Exception) as e:
        await client.some_async_method()
    assert str(e.value) == "Expected error message"
