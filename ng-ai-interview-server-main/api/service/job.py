import uuid
from typing import List, Optional
from api.model.api.job import CreateJobRequest, UpdateJobRequest, JobResponse
from api.model.db.job import Job
from api.repositories.job_repository import JobRepository
from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, DuplicateError

class JobService:
    def __init__(self):
        self.repository = JobRepository()
    
    @log
    async def create_job(self, request: CreateJobRequest) -> JobResponse:
        """Create a new job"""
        # Create job document
        job = Job(
            job_id=str(uuid.uuid4()),
            job_title=request.job_title,
            job_description=request.job_description,
            technical_skills=request.technical_skills,
            soft_skills=request.soft_skills
        )
        
        # Save to database
        job = await self.repository.create_job(job)
        
        return self._to_response(job)
    
    @log
    async def get_job(self, job_id: str) -> JobResponse:
        """Get job by ID"""
        job = await self.repository.get_job_by_id(job_id)
        if not job:
            raise NotFoundError("Job not found")
        
        return self._to_response(job)
    
    @log
    async def get_jobs(self, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Get list of jobs (paginated)"""
        jobs = await self.repository.get_jobs(skip, limit)
        return [self._to_response(job) for job in jobs]
    
    @log
    async def update_job(self, job_id: str, request: UpdateJobRequest) -> JobResponse:
        """Update job"""
        job = await self.repository.get_job_by_id(job_id)
        if not job:
            raise NotFoundError("Job not found")
        
        # Update provided fields
        if request.job_title:
            job.job_title = request.job_title
        if request.job_description:
            job.job_description = request.job_description
        if request.technical_skills:
            job.technical_skills = request.technical_skills
        if request.soft_skills:
            job.soft_skills = request.soft_skills
        
        job = await self.repository.update_job(job)
        return self._to_response(job)
    
    @log
    async def delete_job(self, job_id: str) -> bool:
        """Delete job"""
        job = await self.repository.get_job_by_id(job_id)
        if not job:
            raise NotFoundError("Job not found")
        
        return await self.repository.delete_job(job_id)
    
    @log
    async def search_jobs(self, keyword: str, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Search jobs"""
        jobs = await self.repository.search_jobs(keyword, skip, limit)
        return [self._to_response(job) for job in jobs]
    
    def _to_response(self, job: Job) -> JobResponse:
        """Convert Job document to JobResponse"""
        return JobResponse(
            job_id=job.job_id,
            job_title=job.job_title,
            job_description=job.job_description,
            technical_skills=job.technical_skills,
            soft_skills=job.soft_skills,
            create_date=job.create_date
        ) 