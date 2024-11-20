import pytest
from aio_straico import StraicoClient

def test_client_initialization():
    client = StraicoClient()
    assert client is not None
