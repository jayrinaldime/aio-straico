import pytest

@pytest.fixture
def mock_api_key():
    return "test_key"

@pytest.fixture
def mock_base_url():
    return "http://test.url"
