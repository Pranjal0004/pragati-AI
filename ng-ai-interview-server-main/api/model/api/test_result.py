from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional

class QuestionAnswer(BaseModel):
    """问题答案模型"""
    question_id: Optional[str] = Field(None, description="问题ID")
    question: str = Field(..., description="问题内容")
    answer: str = Field(..., description="回答内容")
    score: Optional[float] = Field(None, description="得分")
    feedback: Optional[str] = Field(None, description="反馈")

class CreateTestResultRequest(BaseModel):
    """创建测试结果请求模型"""
    test_id: str = Field(..., description="测试ID")
    user_id: str = Field(..., description="用户ID")
    summary: str = Field(..., description="总结")
    score: float = Field(..., description="分数", ge=0, le=100)
    question_number: int = Field(..., description="问题数量", ge=0)
    correct_number: int = Field(..., description="正确答案数量", ge=0)
    elapse_time: int = Field(..., description="耗时(分钟)", ge=0)
    qa_history: List[Dict[str, Any]] = Field(..., description="问答历史")
    
    @field_validator('correct_number')
    @classmethod
    def correct_number_must_be_less_than_question_number(cls, v, info):
        if 'question_number' in info.data and v > info.data['question_number']:
            raise ValueError('正确答案数量不能大于问题数量')
        return v

class UpdateTestResultRequest(BaseModel):
    """更新测试结果请求模型"""
    summary: Optional[str] = Field(None, description="总结")
    score: Optional[float] = Field(None, description="分数", ge=0, le=100)
    question_number: Optional[int] = Field(None, description="问题数量", ge=0)
    correct_number: Optional[int] = Field(None, description="正确答案数量", ge=0)
    elapse_time: Optional[int] = Field(None, description="耗时(分钟)", ge=0)
    qa_history: Optional[List[Dict[str, Any]]] = Field(None, description="问答历史")
    
    @field_validator('correct_number')
    @classmethod
    def correct_number_must_be_less_than_question_number(cls, v, info):
        if (v is not None and 'question_number' in info.data and 
            info.data['question_number'] is not None and 
            v > info.data['question_number']):
            raise ValueError('正确答案数量不能大于问题数量')
        return v

class TestResultResponse(BaseModel):
    """测试结果响应模型"""
    test_id: str = Field(..., description="测试ID")
    user_id: str = Field(..., description="用户ID")
    summary: str = Field(..., description="总结")
    score: float = Field(..., description="分数")
    question_number: int = Field(..., description="问题数量")
    correct_number: int = Field(..., description="正确答案数量")
    elapse_time: int = Field(..., description="耗时(分钟)")
    qa_history: List[Dict[str, Any]] = Field(..., description="问答历史")