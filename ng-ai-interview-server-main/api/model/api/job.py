from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class JobBase(BaseModel):
    """Base model for job data"""
    job_title: str = Field(..., description="职位名称")
    job_description: str = Field(..., description="职位描述")
    technical_skills: List[str] = Field(..., description="技术技能要求")
    soft_skills: List[str] = Field(..., description="软技能要求")

class CreateJobRequest(JobBase):
    """Request model for creating a job"""
    pass

class UpdateJobRequest(BaseModel):
    """Request model for updating a job"""
    job_title: Optional[str] = Field(None, description="职位名称")
    job_description: Optional[str] = Field(None, description="职位描述")
    technical_skills: Optional[List[str]] = Field(None, description="技术技能要求")
    soft_skills: Optional[List[str]] = Field(None, description="软技能要求")

class JobResponse(JobBase):
    """Response model for job data"""
    job_id: str = Field(..., description="职位ID")
    create_date: datetime = Field(..., description="创建时间") 