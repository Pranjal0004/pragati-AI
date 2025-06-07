from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from api.model.api.base import Response
from api.model.api.job import CreateJobRequest, UpdateJobRequest, JobResponse
from api.service.job import JobService

router = APIRouter(
    prefix="/job",
    tags=["job"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Response[JobResponse])
async def create_job(request: CreateJobRequest):
    """
    Create a new job
    
    - **job_title**: Job title
    - **job_description**: Job description
    - **technical_skills**: Technical skills required
    - **soft_skills**: Soft skills required
    """
    service = JobService()
    job = await service.create_job(request)
    return Response[JobResponse](data=job)

@router.get("/{job_id}", response_model=Response[JobResponse])
async def get_job(job_id: str):
    """
    Get job by ID
    
    - **job_id**: Job ID
    """
    service = JobService()
    job = await service.get_job(job_id)
    return Response[JobResponse](data=job)

@router.get("", response_model=Response[List[JobResponse]])
async def get_jobs(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Get job list (pagination)
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = JobService()
    jobs = await service.get_jobs(skip, limit)
    return Response[List[JobResponse]](data=jobs)

@router.put("/{job_id}", response_model=Response[JobResponse])
async def update_job(job_id: str, request: UpdateJobRequest):
    """
    Update job
    
    - **job_id**: Job ID
    - **job_title**: Job title (optional)
    - **job_description**: Job description (optional)
    - **technical_skills**: Technical skills required (optional)
    - **soft_skills**: Soft skills required (optional)
    """
    service = JobService()
    job = await service.update_job(job_id, request)
    return Response[JobResponse](data=job)

@router.delete("/{job_id}", response_model=Response[dict])
async def delete_job(job_id: str):
    """
    Delete job
    
    - **job_id**: Job ID
    """
    service = JobService()
    deleted = await service.delete_job(job_id)
    return Response[dict](data={"deleted": deleted})

@router.get("/search/{keyword}", response_model=Response[List[JobResponse]])
async def search_jobs(
    keyword: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """
    Search jobs
    
    - **keyword**: Search keyword
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    service = JobService()
    jobs = await service.search_jobs(keyword, skip, limit)
    return Response[List[JobResponse]](data=jobs) 