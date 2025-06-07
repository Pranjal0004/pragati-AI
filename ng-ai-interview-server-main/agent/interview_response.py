from enum import Enum
from pydantic import BaseModel, Field

class QuestionType(str, Enum):
    SINGLE_CHOICE = "Single Choice"
    MULTIPLE_CHOICE = "Multiple Choice"
    ESSAY = "Essay"
    SHORT_ANSWER = "Short Answer"
    TRUE_FALSE = "True False"
    NONE = "None"


class Question(BaseModel):
    question: str = Field(description="The question of the interview, including choices")
    question_number: int = Field(description="The number of the question, start from 1")
    question_type: QuestionType = Field(description="The type of the question")
    knowledge_point: str = Field(description="The knowledge point of the question")
    answer: str = Field(description="The answer of the question")
    

class Answer(BaseModel):
    is_valid: bool = Field(description="Whether the answer is a valid response")
    giveup: bool = Field(description="Whether the user wants to giveup or skip the question")
    suggest_more_details: bool = Field(description="Answer is too short, suggest more details")
    follow_up_question: str = Field(description="Provide a friendly follow-up question to get more details of the answer")
    feedback: str = Field(description="Provide a friendly feedback to the user")
    is_correct: bool = Field(description="Whether the answer is correct")
    analysis: str = Field(description="The analysis of the answer")
    score: int = Field(description="The score of the answer (0-5)")


class QAResult(BaseModel):
    question: Question = Field(description="The question of the interview")
    answer: Answer = Field(description="The answer of the question")
    is_interview_over: bool = Field(description="Whether the interview is over")
    summary: str = Field(description="The summary of the question and answer")
    

class InterviewResult(BaseModel):
    summary: str = Field(description="The summary of the interview")
    total_question_number: int = Field(description="The total number of questions")
    correct_question_number: int = Field(description="The number of correct questions")
    score: int = Field(description="The score of the interview (0-10)")
    interview_time: int = Field(description="The time of the interview (in minutes)")


