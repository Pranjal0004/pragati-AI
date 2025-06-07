import pytest
import warnings
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect
from api.main import app
from api.conf.config import Config

# Mark all tests in this directory as async
pytestmark = pytest.mark.asyncio

# Filter out warnings
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="Call to deprecated create function FileDescriptor()"
)

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Setup test database connection"""
    # Disconnect any existing connections first
    disconnect(alias='default')
    
    config = Config.load_config()
    
    # Use a test database
    test_db = f"{config.mongodb.database}_test"
    
    # Connect to test database
    connect(
        db=test_db,
        host=config.mongodb.host,
        port=config.mongodb.port,
        username=config.mongodb.username,
        password=config.mongodb.password,
        authentication_source=config.mongodb.authentication_source,
        alias='default'
    )
    
    yield
    
    # Cleanup after tests
    disconnect(alias='default')

@pytest.fixture
async def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def mongo_connection():
    # Connect to the test database
    connect(
        db="test_database_name",  # Replace with your test database name
        host="localhost",
        port=27017
    )
    yield
    # Disconnect
    disconnect() 