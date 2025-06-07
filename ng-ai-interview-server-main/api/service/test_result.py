import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, UTC
from api.model.db.test_result import TestResult
from api.model.api.test_result import TestResultResponse, CreateTestResultRequest
from api.repositories.test_result_repository import TestResultRepository
from api.repositories.test_repository import TestRepository
from api.repositories.user_repository import UserRepository
from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, ValidationError
from loguru import logger

class TestResultService:
    """Test Result Service Class"""
    
    def __init__(self):
        """Initialize Test Result Service"""
        self.repository = TestResultRepository()
        self.test_repository = TestRepository()
        self.user_repository = UserRepository()
    
    @log
    async def complete_test_result(self, request: CreateTestResultRequest) -> TestResultResponse:
        """
        Create or update a test result
        
        Args:
            request: Create test result request
            
        Returns:
            TestResultResponse: Test result response
        """        
        # Check if the result for the test already exists
        existing_result = await self.repository.get_result_by_test_id(request.test_id)        
        if existing_result:
            # If the result exists, update it
            logger.info(f"Test result already exists, updating: {existing_result.test_id}")
            
            # Update fields
            existing_result.summary = request.summary
            existing_result.score = request.score
            existing_result.question_number = request.question_number
            existing_result.correct_number = request.correct_number
            existing_result.elapse_time = request.elapse_time
            existing_result.qa_history = request.qa_history
            
            # Save the update
            updated_result = await self.repository.create_result(existing_result)
            logger.info(f"Test result update completed: {existing_result.test_id}")
            
            return self._to_response(updated_result)
        else:
            # If the result does not exist, create a new one
            test_result = TestResult(
                test_id=request.test_id,
                user_id=request.user_id,
                summary=request.summary,
                score=request.score,
                question_number=request.question_number,
                correct_number=request.correct_number,
                elapse_time=request.elapse_time,
                qa_history=request.qa_history
            )
            
            # Save to the database
            created_result = await self.repository.create_result(test_result)
            logger.info(f"Created new test result: {request.test_id}")
            
            return self._to_response(created_result)


    @log
    async def create_test_result(self, request: CreateTestResultRequest) -> TestResultResponse:
        """
        Create or update a test result
        
        Args:
            request: Create test result request
            
        Returns:
            TestResultResponse: Test result response
            
        Raises:
            NotFoundError: If the test or user does not exist
        """
        # Check if the test exists
        test = await self.test_repository.get_test_by_id(request.test_id)
        if not test:
            raise NotFoundError(f"Test does not exist: {request.test_id}")
        
        # Check if the user exists
        user = await self.user_repository.get_user_by_id(request.user_id)
        if not user:
            raise NotFoundError(f"User does not exist: {request.user_id}")
        
        # Check if the result for the test already exists
        existing_result = await self.repository.get_result_by_test_id(request.test_id)
        
        # Validate data
        if request.score < 0 or request.score > 100:
            raise ValidationError("Score must be between 0 and 100")
        
        if request.question_number < 0:
            raise ValidationError("Number of questions cannot be negative")
            
        if request.correct_number < 0:
            raise ValidationError("Number of correct answers cannot be negative")
            
        if request.correct_number > request.question_number:
            raise ValidationError("Number of correct answers cannot exceed total number of questions")
            
        if request.elapse_time < 0:
            raise ValidationError("Elapsed time cannot be negative")
        
        if existing_result:
            # If the result exists, update it
            logger.info(f"Test result already exists, updating: {existing_result.test_id}")
            
            # Update fields
            existing_result.summary = request.summary
            existing_result.score = request.score
            existing_result.question_number = request.question_number
            existing_result.correct_number = request.correct_number
            existing_result.elapse_time = request.elapse_time
            existing_result.qa_history = request.qa_history
            
            # Save the update
            updated_result = await self.repository.create_result(existing_result)
            logger.info(f"Test result update completed: {existing_result.test_id}")
            
            return self._to_response(updated_result)
        else:
            # If the result does not exist, create a new one
            test_result = TestResult(
                test_id=request.test_id,
                user_id=request.user_id,
                summary=request.summary,
                score=request.score,
                question_number=request.question_number,
                correct_number=request.correct_number,
                elapse_time=request.elapse_time,
                qa_history=request.qa_history
            )
            
            # Save to the database
            created_result = await self.repository.create_result(test_result)
            logger.info(f"Created new test result: {request.test_id}")
            
            return self._to_response(created_result)
    
    @log
    async def get_test_result_by_test_id(self, test_id: str) -> TestResultResponse:
        """
        Get test result by test ID
        
        Args:
            test_id: Test ID
            
        Returns:
            TestResultResponse: Test result response
            
        Raises:
            NotFoundError: If the test result does not exist
        """
        test_result = await self.repository.get_result_by_test_id(test_id)
        if not test_result:
            raise NotFoundError(f"No result found for the test: {test_id}")
        
        return self._to_response(test_result)
    
    @log
    async def get_test_results_by_user_id(self, user_id: str) -> List[TestResultResponse]:
        """
        Get list of test results by user ID
        
        Args:
            user_id: User ID
            
        Returns:
            List[TestResultResponse]: List of test result responses
        """
        test_results = await self.repository.get_results_by_user_id(user_id)
        return [self._to_response(result) for result in test_results]
    
    def _to_response(self, test_result: TestResult) -> TestResultResponse:
        """
        Convert TestResult document to TestResultResponse
        
        Args:
            test_result: Test result document
            
        Returns:
            TestResultResponse: Test result response
        """
        return TestResultResponse(
            test_id=test_result.test_id,
            user_id=test_result.user_id,
            summary=test_result.summary,
            score=test_result.score,
            question_number=test_result.question_number,
            correct_number=test_result.correct_number,
            elapse_time=test_result.elapse_time,
            qa_history=test_result.qa_history
        )
