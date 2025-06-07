from mongoengine import connect, disconnect
from loguru import logger
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def init_mongodb():
    """Test MongoDB connection"""
    try:
        disconnect()
        mongo_uri = os.getenv("MONGODB_URI")  # Fetch MongoDB URI from the environment variable
        if mongo_uri is None:
            raise ValueError("MongoDB URI is not set in the .env file")
        connect(alias="default", host=mongo_uri)
        logger.info("Successfully connected to MongoDB!")
    except Exception as e:
        logger.error(f"Connection failed: {e}")

init_mongodb()
