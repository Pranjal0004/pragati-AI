from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from api.constants.common import QuestionType, Difficulty, Language

class QuestionBase(BaseModel):
    """问题基础模型"""
    question: str = Field(..., description="题目内容")
    answer: str = Field(..., description="答案内容")
    examination_points: List[str] = Field(default=[], description="考查要点")
    job_title: str = Field(..., description="岗位名称")
    language: str = Field(..., description="语言", examples=["English", "Chinese"])
    difficulty: str = Field(..., description="难度", examples=["easy", "medium", "hard"])
    type: str = Field(..., description="题目类型", examples=["multiple_choice", "single_choice", "true_false", "short_answer", "essay"])

class CreateQuestionRequest(QuestionBase):
    """创建问题请求模型"""
    pass

class UpdateQuestionRequest(BaseModel):
    """更新问题请求模型"""
    question: Optional[str] = Field(None, description="题目内容")
    answer: Optional[str] = Field(None, description="答案内容")
    examination_points: Optional[List[str]] = Field(None, description="考查要点")
    job_title: Optional[str] = Field(None, description="岗位名称")
    language: Optional[str] = Field(None, description="语言", examples=["English", "Chinese"])
    difficulty: Optional[str] = Field(None, description="难度", examples=["easy", "medium", "hard"])
    type: Optional[str] = Field(None, description="题目类型", examples=["multiple_choice", "single_choice", "true_false", "short_answer", "essay"])

class QuestionResponse(QuestionBase):
    """问题响应模型"""
    question_id: str = Field(..., description="题目编号") 