from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from api.model.api.base import Response
from api.model.api.question import CreateQuestionRequest, UpdateQuestionRequest, QuestionResponse
from api.service.question import QuestionService

router = APIRouter(
    prefix="/question",
    tags=["question"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Response[QuestionResponse])
async def create_question(request: CreateQuestionRequest):
    """
    Create a new question
    
    - **question**: Question content
    - **answer**: Answer content
    - **examination_points**: Examination points
    - **job_title**: Job title
    - **language**: Language
    - **difficulty**: Difficulty
    - **type**: Question type
    """
    service = QuestionService()
    question = await service.create_question(request)
    return Response[QuestionResponse](data=question)

@router.get("/{question_id}", response_model=Response[QuestionResponse])
async def get_question(question_id: str):
    """
    Get question by ID
    
    - **question_id**: Question ID
    """
    service = QuestionService()
    question = await service.get_question(question_id)
    return Response[QuestionResponse](data=question)

@router.get("", response_model=Response[List[QuestionResponse]])
async def get_questions(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get a list of questions (paginated)
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = QuestionService()
    questions = await service.get_questions(skip, limit)
    return Response[List[QuestionResponse]](data=questions)

@router.put("/{question_id}", response_model=Response[QuestionResponse])
async def update_question(question_id: str, request: UpdateQuestionRequest):
    """
    Update a question
    
    - **question_id**: Question ID
    - **question**: Question content (optional)
    - **answer**: Answer content (optional)
    - **examination_points**: Examination points (optional)
    - **job_title**: Job title (optional)
    - **language**: Language (optional)
    - **difficulty**: Difficulty (optional)
    - **type**: Question type (optional)
    """
    service = QuestionService()
    question = await service.update_question(question_id, request)
    return Response[QuestionResponse](data=question)

@router.delete("/{question_id}", response_model=Response[dict])
async def delete_question(question_id: str):
    """
    Delete a question
    
    - **question_id**: Question ID
    """
    service = QuestionService()
    deleted = await service.delete_question(question_id)
    return Response[dict](data={"deleted": deleted})

@router.get("/search/{keyword}", response_model=Response[List[QuestionResponse]])
async def search_questions(
    keyword: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Search questions
    
    - **keyword**: Search keyword
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = QuestionService()
    questions = await service.search_questions(keyword, skip, limit)
    return Response[List[QuestionResponse]](data=questions)

@router.get("/job/{job_title}", response_model=Response[List[QuestionResponse]])
async def get_questions_by_job_title(
    job_title: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get questions by job title
    
    - **job_title**: Job title
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = QuestionService()
    questions = await service.get_questions_by_job_title(job_title, skip, limit)
    return Response[List[QuestionResponse]](data=questions)

@router.get("/difficulty/{difficulty}", response_model=Response[List[QuestionResponse]])
async def get_questions_by_difficulty(
    difficulty: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get questions by difficulty
    
    - **difficulty**: Difficulty
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = QuestionService()
    questions = await service.get_questions_by_difficulty(difficulty, skip, limit)
    return Response[List[QuestionResponse]](data=questions)

@router.get("/type/{type}", response_model=Response[List[QuestionResponse]])
async def get_questions_by_type(
    type: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get questions by type
    
    - **type**: Question type
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = QuestionService()
    questions = await service.get_questions_by_type(type, skip, limit)
    return Response[List[QuestionResponse]](data=questions) 