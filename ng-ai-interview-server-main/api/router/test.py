from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from api.model.api.base import Response
from api.model.api.test import CreateTestRequest, UpdateTestRequest, TestResponse
from api.service.test import TestService
from api.constants.common import TestType
# from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, DuplicateError, ValidationError
from loguru import logger

router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Response[TestResponse])
async def create_test(request: CreateTestRequest):
    """
    Create a new test
    
    - **test_id**: Test ID
    - **type**: Test type
    - **language**: Language
    - **difficulty**: Difficulty
    - **job_id**: Associated job ID (optional)
    - **user_id**: Associated user ID (optional)
    - **question_ids**: List of question IDs included in the test (optional)
    """
    service = TestService()
    test = await service.create_test(request)
    return Response[TestResponse](data=test)

@router.get("/{test_id}", response_model=Response[TestResponse])
async def get_test(test_id: str):
    """
    Get test by ID
    
    - **test_id**: Test ID
    """
    service = TestService()
    test = await service.get_test(test_id)
    return Response[TestResponse](data=test)

@router.get("", response_model=Response[List[TestResponse]])
async def get_tests(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get a list of tests (paginated)
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = TestService()
    tests = await service.get_tests(skip, limit)
    return Response[List[TestResponse]](data=tests)

@router.put("/{test_id}", response_model=Response[TestResponse])
async def update_test(test_id: str, request: UpdateTestRequest):
    """
    Update a test
    
    - **test_id**: Test ID
    - **type**: Test type (optional)
    - **language**: Language (optional)
    - **difficulty**: Difficulty (optional)
    - **status**: Test status (optional)
    - **job_id**: Associated job ID (optional)
    - **user_id**: Associated user ID (optional)
    - **question_ids**: List of question IDs included in the test (optional)
    """
    service = TestService()
    test = await service.update_test(test_id, request)
    return Response[TestResponse](data=test)

@router.delete("/{test_id}", response_model=Response[dict])
async def delete_test(test_id: str):
    """
    Delete a test
    
    - **test_id**: Test ID
    """
    service = TestService()
    deleted = await service.delete_test(test_id)
    return Response[dict](data={"deleted": deleted})

@router.get("/user/{user_id}", response_model=Response[List[TestResponse]])
async def get_tests_by_user_id(
    user_id: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get tests by user ID
    
    - **user_id**: User ID
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = TestService()
    tests = await service.get_tests_by_user_id(user_id, skip, limit)
    return Response[List[TestResponse]](data=tests)

@router.get("/job/{job_id}", response_model=Response[List[TestResponse]])
async def get_tests_by_job_id(
    job_id: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get tests by job ID
    
    - **job_id**: Job ID
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = TestService()
    tests = await service.get_tests_by_job_id(job_id, skip, limit)
    return Response[List[TestResponse]](data=tests)

@router.get("/status/{status}", response_model=Response[List[TestResponse]])
async def get_tests_by_status(
    status: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get tests by status
    
    - **status**: Test status
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = TestService()
    tests = await service.get_tests_by_status(status, skip, limit)
    return Response[List[TestResponse]](data=tests)

@router.get("/type/{type}", response_model=Response[List[TestResponse]])
async def get_tests_by_type(
    type: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get tests by type
    
    - **type**: Test type, valid values: interview, coding, behavior
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    if type not in TestType.choices():
        raise HTTPException(status_code=400, detail=f"Invalid test type: {type}")
    
    service = TestService()
    tests = await service.get_tests_by_type(type, skip, limit)
    return Response[List[TestResponse]](data=tests) 

@router.get("/activate_code/{code}", response_model=Response[TestResponse])
async def get_test_by_activate_code(code: str):
    """
    Get test by activation code
    
    - **code**: Test activation code
    
    Only returns tests that are not completed
    """
    try:
        service = TestService()
        test = await service.get_test_by_activate_code(code)
        return Response[TestResponse](
            code="0",
            message="success",
            data=test
        )
    except NotFoundError as e:
        logger.warning(f"NotFoundError Failed to get test: {str(e)}, Activation code: {code}")
        return Response[TestResponse](
            code="404",
            message=str(e),
            data=None
        )
    except Exception as e:
        logger.error(f"Exception Failed to get test: {e}, Activation code: {code}")
        raise HTTPException(status_code=500, detail=str(e))