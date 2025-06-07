import pytest
import warnings
from fastapi.testclient import TestClient
from api.main import app

# Filter out the specific deprecation warning from protobuf
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="Call to deprecated create function FileDescriptor()"
)

@pytest.fixture
def client():
    """
    Test client fixture that can be used across all API tests
    """
    return TestClient(app) 