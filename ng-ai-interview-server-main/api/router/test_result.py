from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from api.model.api.base import Response
from api.model.api.test_result import CreateTestResultRequest, UpdateTestResultRequest, TestResultResponse
from api.service.test_result import TestResultService
from api.exceptions.api_error import NotFoundError, ValidationError
from loguru import logger

router = APIRouter(
    prefix="/test_result",
    tags=["test_result"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Response[TestResultResponse])
async def create_test_result(request: CreateTestResultRequest):
    """
    Create or update test result
    
    - **test_id**: Test ID
    - **user_id**: User ID
    - **summary**: Summary
    - **score**: Score (0-100)
    - **question_number**: Number of questions
    - **correct_number**: Number of correct answers
    - **elapse_time**: Elapsed time (minutes)
    - **qa_history**: Q&A history
    """
    try:
        service = TestResultService()
        result = await service.create_test_result(request)
        return Response[TestResultResponse](
            code="0",
            message="success",
            data=result
        )
    except NotFoundError as e:
        logger.warning(f"NotFoundError Failed to create test result: {str(e)}")
        return Response[TestResultResponse](
            code="404",
            message=str(e),
            data=None
        )
    except ValidationError as e:
        logger.warning(f"ValidationError Failed to create test result: {str(e)}")
        return Response[TestResultResponse](
            code="400",
            message=str(e),
            data=None
        )
    except Exception as e:
        logger.error(f"Exception Failed to create test result: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test/{test_id}", response_model=Response[TestResultResponse])
async def get_test_result_by_test_id(test_id: str):
    """
    Get test result by test ID
    
    - **test_id**: Test ID
    """
    try:
        service = TestResultService()
        result = await service.get_test_result_by_test_id(test_id)
        return Response[TestResultResponse](
            code="0",
            message="success",
            data=result
        )
    except NotFoundError as e:
        logger.warning(f"NotFoundError Failed to get test result: {str(e)}, Test ID: {test_id}")
        return Response[TestResultResponse](
            code="404",
            message=str(e),
            data=None
        )
    except Exception as e:
        logger.error(f"Exception Failed to get test result: {e}, Test ID: {test_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=Response[List[TestResultResponse]])
async def get_test_results_by_user_id(user_id: str):
    """
    Get test result list by user ID
    
    - **user_id**: User ID
    """
    try:
        service = TestResultService()
        results = await service.get_test_results_by_user_id(user_id)
        return Response[List[TestResultResponse]](
            code="0",
            message="success",
            data=results
        )
    except Exception as e:
        logger.error(f"Exception Failed to get user test results: {e}, User ID: {user_id}")
        raise HTTPException(status_code=500, detail=str(e))