from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from api.model.api.base import Response
from api.model.api.chat import StartChatRequest, AnswerRequest, ChatResponse
from api.service.chat import ChatService
from api.utils.log_decorator import log
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4

router = APIRouter(prefix="/chat", tags=["Chat"])

# Service instance
chat_service = ChatService()

@router.post("/start", response_model=Response[ChatResponse])
@log
async def start_chat(request: StartChatRequest):
    """
    Start Chat
    
    Start a new interview chat session and return the first question
    """
    try:
        # Call service layer method
        result = await chat_service.start_chat(
            user_id=request.user_id,
            test_id=request.test_id,
            job_title=request.job_title,
            examination_points=request.examination_points,
            test_time=request.test_time,
            language=request.language,
            difficulty=request.difficulty
        )
        
        # Return success response
        return Response[ChatResponse](
            code="0",
            message="success",
            data=result
        )
    except Exception as e:
        # Handle exception
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/answer", response_model=Response[ChatResponse])
@log
async def answer_question(request: AnswerRequest):
    """
    Answer Question
    
    Submit the user's answer to a question and get the next question or feedback
    """
    try:
        # Call service layer method
        result = await chat_service.process_answer(
            user_id=request.user_id,
            test_id=request.test_id,
            question_id=request.question_id,
            user_answer=request.user_answer
        )
        
        # Return success response
        return Response[ChatResponse](
            code="0",
            message="success",
            data=result
        )
    except Exception as e:
        # Handle exception
        raise HTTPException(status_code=500, detail=str(e))