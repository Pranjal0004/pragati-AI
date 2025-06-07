import uuid
from typing import List, Optional
from api.model.api.question import CreateQuestionRequest, UpdateQuestionRequest, QuestionResponse
from api.model.db.question import Question
from api.repositories.question_repository import QuestionRepository
from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, DuplicateError

class QuestionService:
    def __init__(self):
        self.repository = QuestionRepository()
    
    @log
    async def create_question(self, request: CreateQuestionRequest) -> QuestionResponse:
        """Create a new question"""
        # Create question document
        question = Question(
            question_id=str(uuid.uuid4()),
            question=request.question,
            answer=request.answer,
            examination_points=request.examination_points,
            job_title=request.job_title,
            language=request.language,
            difficulty=request.difficulty,
            type=request.type
        )
        
        # Save to database
        question = await self.repository.create_question(question)
        
        return self._to_response(question)
    
    @log
    async def get_question(self, question_id: str) -> QuestionResponse:
        """Get question by ID"""
        question = await self.repository.get_question_by_id(question_id)
        if not question:
            raise NotFoundError("Question not found")
        
        return self._to_response(question)
    
    @log
    async def get_questions(self, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """Get list of questions (paginated)"""
        questions = await self.repository.get_questions(skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def update_question(self, question_id: str, request: UpdateQuestionRequest) -> QuestionResponse:
        """Update question"""
        question = await self.repository.get_question_by_id(question_id)
        if not question:
            raise NotFoundError("Question not found")
        
        # Update provided fields
        if request.question is not None:
            question.question = request.question
        if request.answer is not None:
            question.answer = request.answer
        if request.examination_points is not None:
            question.examination_points = request.examination_points
        if request.job_title is not None:
            question.job_title = request.job_title
        if request.language is not None:
            question.language = request.language
        if request.difficulty is not None:
            question.difficulty = request.difficulty
        if request.type is not None:
            question.type = request.type
        
        question = await self.repository.update_question(question)
        return self._to_response(question)
    
    @log
    async def delete_question(self, question_id: str) -> bool:
        """Delete question"""
        question = await self.repository.get_question_by_id(question_id)
        if not question:
            raise NotFoundError("Question not found")
        
        return await self.repository.delete_question(question_id)
    
    @log
    async def search_questions(self, keyword: str, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """Search questions"""
        questions = await self.repository.search_questions(keyword, skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def get_questions_by_job_title(self, job_title: str, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """Get questions by job title"""
        questions = await self.repository.get_questions_by_job_title(job_title, skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def get_questions_by_examination_points(self, examination_points: List[str], skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """Get questions by examination points"""
        questions = await self.repository.get_questions_by_examination_points(examination_points, skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def get_questions_by_difficulty(self, difficulty: str, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """Get questions by difficulty"""
        questions = await self.repository.get_questions_by_difficulty(difficulty, skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def get_questions_by_type(self, type: str, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """Get questions by type"""
        questions = await self.repository.get_questions_by_type(type, skip, limit)
        return [self._to_response(question) for question in questions]
    
    def _to_response(self, question: Question) -> QuestionResponse:
        """Convert Question document to QuestionResponse"""
        return QuestionResponse(
            question_id=question.question_id,
            question=question.question,
            answer=question.answer,
            examination_points=question.examination_points,
            job_title=question.job_title,
            language=question.language,
            difficulty=question.difficulty,
            type=question.type
        ) 