from typing import Optional, List
from loguru import logger
from api.model.db.test import Test, TestStatus
from api.utils.log_decorator import log
from datetime import datetime, UTC  
from mongoengine import Document, StringField, DateTimeField

class TestRepository:
    def __init__(self):
        # Assuming you are using MongoEngine
        self.collection = Test._get_collection()  # Get the underlying MongoDB collection

    @log
    async def create_test(self, test: Test) -> Test:
        """Create a new test"""
        return test.save()
    
    @log
    async def get_test_by_id(self, test_id: str) -> Optional[Test]:
        """Get a test by ID"""
        return Test.objects(test_id=test_id).first()
    
    @log
    async def get_tests(self, skip: int = 0, limit: int = 100) -> List[Test]:
        """Get a list of tests (paginated)"""
        return Test.objects().skip(skip).limit(limit).all()
        
    @log
    async def delete_test(self, test_id: str) -> bool:
        """Delete a test"""
        result = Test.objects(test_id=test_id).delete()
        return result > 0
    
    @log
    async def get_tests_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Test]:
        """Get tests by user ID"""
        return Test.objects(user_id=user_id).skip(skip).limit(limit).all()
    
    @log
    async def get_tests_by_job_id(self, job_id: str, skip: int = 0, limit: int = 100) -> List[Test]:
        """Get tests by job ID"""
        return Test.objects(job_id=job_id).skip(skip).limit(limit).all()
    
    @log
    async def get_tests_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Test]:
        """Get tests by status"""
        return Test.objects(status=status).skip(skip).limit(limit).all()
    
    @log
    async def get_tests_by_type(self, type: str, skip: int = 0, limit: int = 100) -> List[Test]:
        """Get tests by type"""
        return Test.objects(type=type).skip(skip).limit(limit).all()
    
    @log
    async def get_test_by_activate_code(self, activate_code: str) -> Optional[Test]:
        """Get a test by activation code"""
        return Test.objects(activate_code=activate_code).first()
    
    @log
    async def update_test_status(self, test_id: str, status: TestStatus) -> Optional[Test]:
        """
        Update test status
        
        Args:
            test_id: Test ID
            status: New status
            
        Returns:
            Optional[Test]: Updated test document, or None if not found
        """
        try:
            test = Test.objects(test_id=test_id).first()
            if test:
                test.status = status.value
                test.update_date = datetime.now(UTC)
                if status == TestStatus.COMPLETED:
                    test.close_date = datetime.now(UTC)
                test.save()
                logger.info(f"Successfully updated test status: {test_id} -> {status}")
                return test
            logger.info(f"Test not found: {test_id}")
            return None
        except Exception as e:
            logger.error(f"Failed to update test status: {e}")
            raise 