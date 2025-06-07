from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from api.constants.common import TestType, Difficulty, Language, TestStatus

class TestBase(BaseModel):
    """测试基础模型"""
    type: str = Field(..., description="测试类型", examples=TestType.choices())
    language: str = Field(..., description="语言", examples=Language.choices())
    difficulty: str = Field(..., description="难度", examples=Difficulty.choices())

class CreateTestRequest(TestBase):
    """创建测试请求模型"""
    job_id: Optional[str] = Field(None, description="关联的职位ID")
    user_id: Optional[str] = Field(None, description="关联的用户ID")
    question_ids: Optional[List[str]] = Field(None, description="测试包含的问题ID列表")
    examination_points: Optional[List[str]] = Field(None, description="考查要点列表")
    test_time: Optional[int] = Field(None, description="测试时间（分钟）", ge=1, le=120)

class UpdateTestRequest(BaseModel):
    """更新测试请求模型"""
    type: Optional[str] = Field(None, description="测试类型", examples=TestType.choices())
    language: Optional[str] = Field(None, description="语言", examples=Language.choices())
    difficulty: Optional[str] = Field(None, description="难度", examples=Difficulty.choices())
    status: Optional[str] = Field(None, description="测试状态", examples=TestStatus.choices())
    job_id: Optional[str] = Field(None, description="关联的职位ID")
    user_id: Optional[str] = Field(None, description="关联的用户ID")
    question_ids: Optional[List[str]] = Field(None, description="测试包含的问题ID列表")
    examination_points: Optional[List[str]] = Field(None, description="考查要点列表")
    test_time: Optional[int] = Field(None, description="测试时间（分钟）", ge=1, le=120)

class TestResponse(TestBase):
    """测试响应模型"""
    test_id: str = Field(..., description="测试ID")
    activate_code: str = Field(..., description="测试激活码")
    status: str = Field(..., description="测试状态", examples=TestStatus.choices())
    job_id: Optional[str] = Field(None, description="关联的职位ID")
    job_title: Optional[str] = Field(None, description="关联的职位名称")
    user_id: Optional[str] = Field(None, description="关联的用户ID")
    user_name: Optional[str] = Field(None, description="关联的用户名称")
    question_ids: List[str] = Field(default=[], description="测试包含的问题ID列表")
    examination_points: List[str] = Field(default=[], description="考查要点列表")
    test_time: int = Field(..., description="测试时间（分钟）")
    create_date: datetime = Field(..., description="创建时间")
    start_date: datetime = Field(..., description="开始时间")
    expire_date: datetime = Field(..., description="过期时间")
    update_date: Optional[datetime] = Field(None, description="更新时间") 