import pytest
import uuid
from unittest.mock import patch, MagicMock
from datetime import datetime, UTC

from api.model.db.test_result import TestResult
from api.model.api.test_result import CreateTestResultRequest
from api.service.test_result import TestResultService
from api.exceptions.api_error import NotFoundError, ValidationError

@pytest.mark.asyncio
async def test_create_test_result_new():
    """Test creating a new test result"""
    # Create request data
    test_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    request = CreateTestResultRequest(
        test_id=test_id,
        user_id=user_id,
        summary="Test summary",
        score=85.5,
        question_number=10,
        correct_number=8,
        elapse_time=30,
        qa_history=[
            {"question": "What is Python?", "answer": "Python is a high-level programming language"},
            {"question": "What is FastAPI?", "answer": "FastAPI is a modern Python web framework"}
        ]
    )
    
    # Mock test and user existence checks
    with patch('api.repositories.test_repository.TestRepository.get_test_by_id') as mock_get_test, \
         patch('api.repositories.user_repository.UserRepository.get_user_by_id') as mock_get_user, \
         patch('api.repositories.test_result_repository.TestResultRepository.get_result_by_test_id') as mock_get_result, \
         patch('api.repositories.test_result_repository.TestResultRepository.create_result') as mock_create:
        
        # Set mock return values
        mock_get_test.return_value = MagicMock(test_id=test_id)
        mock_get_user.return_value = MagicMock(user_id=user_id)
        mock_get_result.return_value = None  # No existing result
        
        # Set the return value for creating a result
        created_result = TestResult(
            test_id=test_id,
            user_id=user_id,
            summary="Test summary",
            score=85.5,
            question_number=10,
            correct_number=8,
            elapse_time=30,
            qa_history=[
                {"question": "What is Python?", "answer": "Python is a high-level programming language"},
                {"question": "What is FastAPI?", "answer": "FastAPI is a modern Python web framework"}
            ]
        )
        mock_create.return_value = created_result
        
        # Call the service method
        service = TestResultService()
        result = await service.create_test_result(request)
        
        # Validate the result
        assert result.test_id == test_id
        assert result.user_id == user_id
        assert result.summary == "Test summary"
        assert result.score == 85.5
        assert result.question_number == 10
        assert result.correct_number == 8
        assert result.elapse_time == 30
        assert len(result.qa_history) == 2
        
        # Validate method calls
        mock_get_test.assert_called_once_with(test_id)
        mock_get_user.assert_called_once_with(user_id)
        mock_get_result.assert_called_once_with(test_id)
        mock_create.assert_called_once()

@pytest.mark.asyncio
async def test_create_test_result_update_existing():
    """Test updating an existing test result"""
    # Create request data
    test_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    request = CreateTestResultRequest(
        test_id=test_id,
        user_id=user_id,
        summary="Updated summary",
        score=90.0,
        question_number=10,
        correct_number=9,
        elapse_time=25,
        qa_history=[
            {"question": "Question 1", "answer": "Answer 1"},
            {"question": "Question 2", "answer": "Answer 2"}
        ]
    )
    
    # Mock test and user existence checks
    with patch('api.repositories.test_repository.TestRepository.get_test_by_id') as mock_get_test, \
         patch('api.repositories.user_repository.UserRepository.get_user_by_id') as mock_get_user, \
         patch('api.repositories.test_result_repository.TestResultRepository.get_result_by_test_id') as mock_get_result, \
         patch('api.repositories.test_result_repository.TestResultRepository.create_result') as mock_update:
        
        # Set mock return values
        mock_get_test.return_value = MagicMock(test_id=test_id)
        mock_get_user.return_value = MagicMock(user_id=user_id)
        
        # Set the existing result
        existing_result = TestResult(
            test_id=test_id,
            user_id=user_id,
            summary="Original summary",
            score=85.0,
            question_number=10,
            correct_number=7,
            elapse_time=30,
            qa_history=[{"question": "Old question", "answer": "Old answer"}]
        )
        mock_get_result.return_value = existing_result
        
        # Set the return value for updating the result
        updated_result = TestResult(
            test_id=test_id,
            user_id=user_id,
            summary="Updated summary",
            score=90.0,
            question_number=10,
            correct_number=9,
            elapse_time=25,
            qa_history=[
                {"question": "Question 1", "answer": "Answer 1"},
                {"question": "Question 2", "answer": "Answer 2"}
            ]
        )
        mock_update.return_value = updated_result
        
        # Call the service method
        service = TestResultService()
        result = await service.create_test_result(request)
        
        # Validate the result
        assert result.test_id == test_id
        assert result.summary == "Updated summary"
        assert result.score == 90.0
        assert result.question_number == 10
        assert result.correct_number == 9
        assert result.elapse_time == 25
        assert len(result.qa_history) == 2
        
        # Validate method calls
        mock_get_result.assert_called_once_with(test_id)
        mock_update.assert_called_once()

@pytest.mark.asyncio
async def test_get_test_result_by_test_id():
    """Test getting a test result by test ID"""
    test_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    # Mock repository method
    with patch('api.repositories.test_result_repository.TestResultRepository.get_result_by_test_id') as mock_get:
        # Set mock return value
        test_result = TestResult(
            test_id=test_id,
            user_id=user_id,
            summary="Test summary",
            score=85.5,
            question_number=10,
            correct_number=8,
            elapse_time=30,
            qa_history=[{"question": "Question", "answer": "Answer"}]
        )
        mock_get.return_value = test_result
        
        # Call the service method
        service = TestResultService()
        result = await service.get_test_result_by_test_id(test_id)
        
        # Validate the result
        assert result.test_id == test_id
        assert result.user_id == user_id
        assert result.summary == "Test summary"
        assert result.score == 85.5
        assert result.question_number == 10
        assert result.correct_number == 8
        assert result.elapse_time == 30
        
        # Validate method call
        mock_get.assert_called_once_with(test_id)

@pytest.mark.asyncio
async def test_get_test_result_by_test_id_not_found():
    """Test getting a non-existent test result"""
    test_id = str(uuid.uuid4())
    
    # Mock repository method
    with patch('api.repositories.test_result_repository.TestResultRepository.get_result_by_test_id') as mock_get:
        # Set mock return value
        mock_get.return_value = None
        
        # Call the service method and validate exception
        service = TestResultService()
        with pytest.raises(NotFoundError) as excinfo:
            await service.get_test_result_by_test_id(test_id)
        
        # Validate exception message
        assert "No result found for the test" in str(excinfo.value)
        
        # Validate method call
        mock_get.assert_called_once_with(test_id)

@pytest.mark.asyncio
async def test_get_test_results_by_user_id():
    """Test getting a list of test results by user ID"""
    user_id = str(uuid.uuid4())
    
    # Mock repository method
    with patch('api.repositories.test_result_repository.TestResultRepository.get_results_by_user_id') as mock_get:
        # Set mock return value
        test_results = [
            TestResult(
                test_id=str(uuid.uuid4()),
                user_id=user_id,
                summary="Test summary 1",
                score=85.5,
                question_number=10,
                correct_number=8,
                elapse_time=30,
                qa_history=[]
            ),
            TestResult(
                test_id=str(uuid.uuid4()),
                user_id=user_id,
                summary="Test summary 2",
                score=90.0,
                question_number=10,
                correct_number=9,
                elapse_time=25,
                qa_history=[]
            )
        ]
        mock_get.return_value = test_results
        
        # Call the service method
        service = TestResultService()
        results = await service.get_test_results_by_user_id(user_id)
        
        # Validate the results
        assert len(results) == 2
        assert all(r.user_id == user_id for r in results)
        assert results[0].summary == "Test summary 1"
        assert results[1].summary == "Test summary 2"
        
        # Validate method call
        mock_get.assert_called_once_with(user_id)
