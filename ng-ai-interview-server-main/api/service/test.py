import uuid
import random
import string
from typing import List, Optional
from datetime import datetime, UTC, timedelta
from api.model.api.test import CreateTestRequest, UpdateTestRequest, TestResponse
from api.model.db.test import Test
from api.repositories.test_repository import TestRepository
from api.repositories.job_repository import JobRepository
from api.repositories.user_repository import UserRepository
from api.repositories.question_repository import QuestionRepository
from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, DuplicateError, ValidationError
from api.constants.common import TestStatus, TestType, Language, Difficulty
from loguru import logger

class TestService:
    def __init__(self):
        self.repository = TestRepository()
        self.job_repository = JobRepository()
        self.user_repository = UserRepository()
        self.question_repository = QuestionRepository()
    
    def _generate_activate_code(self, length=4) -> str:
        """Generate a numeric activation code of the specified length, default is 4 digits."""
        return ''.join(random.choices(string.digits, k=length))
    
    async def _is_activate_code_unique(self, code: str) -> bool:
        """Check if the activation code is unique."""
        test = await self.repository.get_test_by_activate_code(code)
        return test is None
    
    async def _generate_unique_activate_code(self, length=4) -> str:
        """Generate a unique activation code, starting with a default length of 4."""
        max_attempts = 10  # Maximum number of attempts
        for _ in range(max_attempts):
            code = self._generate_activate_code(length)
            if await self._is_activate_code_unique(code):
                return code
        
        # If unable to generate a unique activation code after multiple attempts, use a longer code
        return await self._generate_unique_activate_code(length + 1)
    
    @log
    async def create_test(self, request: CreateTestRequest) -> TestResponse:
        """Create a new test."""
        # Validate test type
        if request.type not in TestType.choices():
            raise ValidationError(f"Invalid test type: {request.type}")
        
        # Validate language
        if request.language not in Language.choices():
            raise ValidationError(f"Invalid language: {request.language}")
        
        # Validate difficulty
        if request.difficulty not in Difficulty.choices():
            raise ValidationError(f"Invalid difficulty: {request.difficulty}")
        
        # Generate unique ID
        test_id = str(uuid.uuid4())
        
        # Generate unique activation code
        activate_code = await self._generate_unique_activate_code()
        
        # Get Job information
        job_title = None
        if request.job_id:
            job = await self.job_repository.get_job_by_id(request.job_id)
            if job:
                job_title = job.job_title
        
        # Get User information
        user_name = None
        if request.user_id:
            user = await self.user_repository.get_user_by_id(request.user_id)
            if user:
                user_name = user.user_name
        
        # Automatically generate question list
        question_ids = []
        if not request.question_ids:
            pass
            # question_ids = await self._generate_questions(
            #     job_title, 
            #     request.language, 
            #     request.difficulty, 
            #     request.examination_points or []
            # )
        else:
            question_ids = request.question_ids
        
        # Create test document
        test = Test(
            test_id=test_id,
            activate_code=activate_code,
            type=request.type,
            language=request.language,
            difficulty=request.difficulty,
            status=TestStatus.OPEN,
            job_id=request.job_id,
            job_title=job_title,
            user_id=request.user_id,
            user_name=user_name,
            question_ids=question_ids,
            examination_points=request.examination_points or [],
            test_time=request.test_time or 60,  # Default 60 minutes
            create_date=datetime.now(UTC),
            start_date=datetime.now(UTC),
            expire_date=datetime.now(UTC) + timedelta(days=7),  # Default expiration after 7 days
            update_date=datetime.now(UTC)
        )
        
        # Save to database
        test = await self.repository.create_test(test)
        
        return self._to_response(test)
    
    @log
    async def get_test(self, test_id: str) -> TestResponse:
        """Get a test by ID."""
        test = await self.repository.get_test_by_id(test_id)
        if not test:
            raise NotFoundError("Test not found")
        
        return self._to_response(test)
    
    @log
    async def get_tests(self, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """Get a list of tests (paginated)."""
        tests = await self.repository.get_tests(skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def update_test(self, test_id: str, request: UpdateTestRequest) -> TestResponse:
        """Update a test."""
        test = await self.repository.get_test_by_id(test_id)
        if not test:
            raise NotFoundError("Test not found")
        
        # Update provided fields
        if request.type is not None:
            test.type = request.type
        if request.language is not None:
            test.language = request.language
        if request.difficulty is not None:
            test.difficulty = request.difficulty
        if request.status is not None:
            test.status = request.status
        if request.job_id is not None:
            test.job_id = request.job_id
        if request.user_id is not None:
            test.user_id = request.user_id
        if request.question_ids is not None:
            test.question_ids = request.question_ids
        if request.examination_points is not None:
            test.examination_points = request.examination_points
        if request.test_time is not None:
            test.test_time = request.test_time
        
        # Update timestamp
        test.update_date = datetime.now(UTC)
        
        test = await self.repository.update_test(test)
        return self._to_response(test)
    
    @log
    async def delete_test(self, test_id: str) -> bool:
        """Delete a test."""
        test = await self.repository.get_test_by_id(test_id)
        if not test:
            raise NotFoundError("Test not found")
        
        return await self.repository.delete_test(test_id)
    
    @log
    async def get_tests_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """Get tests by user ID."""
        tests = await self.repository.get_tests_by_user_id(user_id, skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def get_tests_by_job_id(self, job_id: str, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """Get tests by job ID."""
        tests = await self.repository.get_tests_by_job_id(job_id, skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def get_tests_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """Get tests by status."""
        tests = await self.repository.get_tests_by_status(status, skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def get_tests_by_type(self, type: str, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """Get tests by type."""
        tests = await self.repository.get_tests_by_type(type, skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def get_test_by_activate_code(self, code: str) -> TestResponse:
        """
        Get a test by activation code (only returns incomplete tests).
        
        Args:
            code: Test activation code
            
        Returns:
            TestResponse: Test response object
            
        Raises:
            NotFoundError: If the test does not exist or is already completed
        """
        # Get test using activation code
        test = await self.repository.get_test_by_activate_code(code)
        logger.info(f"Retrieved test: {test.test_id} {test.status}")
        
        # Check if the test exists
        if not test:
            raise NotFoundError("Test not found")
        
        # Check if the test status is already completed
        if test.status == TestStatus.COMPLETED.value:
            raise NotFoundError("Test already completed")
        
        test_response = self._to_response(test)
        logger.info(f"Test response: {test_response}")
        return test_response
    
    @log
    async def update_test_status_to_completed(self, test_id: str) -> TestResponse:
        """
        Update test status to completed.
        
        Args:
            test_id: Test ID
            
        Returns:
            TestResponse: Updated test response
            
        Raises:
            NotFoundError: If the test does not exist or update fails
        """
        try:
            # Update status using atomic operation
            updated_test = await self.repository.update_test_status(
                test_id=test_id,
                status=TestStatus.COMPLETED,
            )
            
            if not updated_test:
                logger.warning(f"Test not found: {test_id}")
            else:            
                logger.info(f"Test status updated to completed: {test_id}")
                
            return self._to_response(updated_test)
        
        except Exception as e:
            logger.error(f"Failed to update test status: {str(e)}")
            raise
    
    def _to_response(self, test: Test) -> TestResponse:
        """Convert Test document to TestResponse."""
        return TestResponse(
            test_id=test.test_id,
            activate_code=test.activate_code,
            type=test.type,
            language=test.language,
            difficulty=test.difficulty,
            status=test.status,
            job_id=test.job_id,
            job_title=test.job_title,
            user_id=test.user_id,
            user_name=test.user_name,
            question_ids=test.question_ids,
            examination_points=test.examination_points,
            test_time=test.test_time,
            create_date=test.create_date,
            start_date=test.start_date,
            expire_date=test.expire_date,
            update_date=test.update_date
        ) 