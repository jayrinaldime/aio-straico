import pytest
from aio_straico import StraicoClient
from unittest.mock import patch, MagicMock

def test_client_initialization():
    client = StraicoClient()
    assert client is not None

def test_client_initialization_with_custom_params():
    client = StraicoClient(api_key="test_key", base_url="http://test.url")
    assert client.api_key == "test_key"
    assert client.base_url == "http://test.url"

@patch('aio_straico.StraicoClient.some_method')
def test_client_method_call(mock_method):
    client = StraicoClient()
    mock_method.return_value = "mocked response"
    response = client.some_method()
    assert response == "mocked response"
    mock_method.assert_called_once()

def test_client_error_handling():
    client = StraicoClient()
    with pytest.raises(Exception) as e:
        client.some_method()
    assert str(e.value) == "Expected error message"
