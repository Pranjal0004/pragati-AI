from typing import Optional, List
from loguru import logger
from api.model.db.job import Job
from api.utils.log_decorator import log

class JobRepository:
    @log
    async def create_job(self, job: Job) -> Job:
        """Create a new job"""
        return job.save()
    
    @log
    async def get_job_by_id(self, job_id: str) -> Optional[Job]:
        """Get a job by ID"""
        return Job.objects(job_id=job_id).first()
    
    @log
    async def get_jobs(self, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get a list of jobs (paginated)"""
        return Job.objects().skip(skip).limit(limit).all()
    
    @log
    async def update_job(self, job: Job) -> Job:
        """Update a job"""
        return job.save()
    
    @log
    async def delete_job(self, job_id: str) -> bool:
        """Delete a job"""
        result = Job.objects(job_id=job_id).delete()
        return result > 0
    
    @log
    async def search_jobs(self, keyword: str, skip: int = 0, limit: int = 100) -> List[Job]:
        """Search for jobs"""
        return Job.objects(
            job_title__icontains=keyword
        ).skip(skip).limit(limit).all() 