from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class StartChatRequest(BaseModel):
    """开始聊天请求模型"""
    user_id: str = Field(..., description="用户ID")
    test_id: str = Field(..., description="测试ID")
    job_title: str = Field(..., description="职位名称")
    examination_points: str = Field(..., description="考查要点")
    test_time: int = Field(..., description="测试时间（分钟）")
    language: str = Field(..., description="语言")
    difficulty: str = Field(..., description="难度")

class AnswerRequest(BaseModel):
    """回答问题请求模型"""
    user_id: str = Field(..., description="用户ID")
    test_id: str = Field(..., description="测试ID")
    question_id: str = Field(..., description="问题ID")
    user_answer: str = Field(..., description="用户回答")

class ChatResponse(BaseModel):
    """聊天响应模型"""
    qa_history: Optional[List[Dict[str, Any]]] = Field(None, description="问答历史")
    feedback: Optional[str] = Field(None, description="反馈内容")
    type: Optional[str] = Field(None, description="反馈类型", examples=["question", "feedback", "summary"])
    question_id: Optional[str] = Field(None, description="问题ID") 
    is_over: bool = Field(..., description="是否结束")