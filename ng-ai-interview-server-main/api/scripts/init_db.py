from loguru import logger
from api.infra.mongo.connection import init_mongodb
from api.model.db.test import Test
from api.model.db.user import User
from api.model.db.job import Job
from api.model.db.test_result import TestResult
from api.model.db.question import Question

def init_collections():
    """Initialize database collections"""
    try:
        # Connect to MongoDB
        init_mongodb()
        
        # Create collections and indexes
        Test.ensure_indexes()
        User.ensure_indexes()
        Job.ensure_indexes()
        TestResult.ensure_indexes()
        Question.ensure_indexes()
        
        logger.info("Database collections initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize collections: {str(e)}")
        raise

if __name__ == "__main__":
    init_collections() 