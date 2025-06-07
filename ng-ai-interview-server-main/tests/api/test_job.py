import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.main import app
from datetime import datetime, UTC
import uuid

client = TestClient(app)

# Mock job data
@pytest.fixture
def mock_job():
    job = MagicMock()
    job.job_id = str(uuid.uuid4())
    job.job_title = "Frontend Developer"
    job.job_description = "Responsible for the development and maintenance of the company's frontend products"
    job.technical_skills = ["React", "Vue", "JavaScript"]
    job.soft_skills = ["Communication skills", "Team collaboration"]
    job.create_date = datetime.now(UTC)
    return job


class TestJobAPI:
    """Job API Test Class"""

    @patch("api.repositories.job_repository.JobRepository.create_job")
    def test_create_job(self, mock_create_job, mock_job):
        """Test creating a job"""
        # Set mock return value
        mock_create_job.return_value = mock_job
        
        # Send request
        response = client.post(
            "/api/v1/job",
            json={
                "job_title": "Frontend Developer",
                "job_description": "Responsible for the development and maintenance of the company's frontend products",
                "technical_skills": ["React", "Vue", "JavaScript"],
                "soft_skills": ["Communication skills", "Team collaboration"]
            }
        )
        
        # Validate response
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert "job_id" in data["data"]
        assert data["data"]["job_title"] == "Frontend Developer"
        
        # Validate mock call
        mock_create_job.assert_called_once()

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    def test_get_job(self, mock_get_job_by_id, mock_job):
        """Test retrieving a job"""
        # Set mock return value
        mock_get_job_by_id.return_value = mock_job
        
        # Send request
        response = client.get(f"/api/v1/job/{mock_job.job_id}")
        
        # Validate response
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["job_title"] == "Frontend Developer"
        assert data["data"]["job_description"] == "Responsible for the development and maintenance of the company's frontend products"
        assert "React" in data["data"]["technical_skills"]
        
        # Validate mock call
        mock_get_job_by_id.assert_called_once_with(mock_job.job_id)

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    def test_get_job_not_found(self, mock_get_job_by_id):
        """Test retrieving a non-existent job"""
        # Set mock return value
        mock_get_job_by_id.return_value = None
        
        # Send request
        response = client.get("/api/v1/job/nonexistent")
        
        # Validate response
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "404"
        assert "Job not found" in data["message"]
        
        # Validate mock call
        mock_get_job_by_id.assert_called_once_with("nonexistent")

    @patch("api.repositories.job_repository.JobRepository.get_jobs")
    def test_get_jobs(self, mock_get_jobs, mock_job):
        """Test retrieving a list of jobs"""
        # Set mock return value
        mock_get_jobs.return_value = [mock_job]
        
        # Send request
        response = client.get("/api/v1/job?skip=0&limit=10")
        
        # Validate response
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert len(data["data"]) == 1
        assert data["data"][0]["job_title"] == "Frontend Developer"
        
        # Validate mock call
        mock_get_jobs.assert_called_once()

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    @patch("api.repositories.job_repository.JobRepository.update_job")
    def test_update_job(self, mock_update_job, mock_get_job_by_id, mock_job):
        """Test updating a job"""
        # Set mock return value
        mock_get_job_by_id.return_value = mock_job
        mock_update_job.return_value = mock_job
        
        # Send request
        response = client.put(
            f"/api/v1/job/{mock_job.job_id}",
            json={
                "job_title": "Senior Frontend Developer",
                "job_description": "Responsible for frontend architecture design and team management",
                "technical_skills": ["React", "Vue", "TypeScript", "Webpack"],
                "soft_skills": ["Leadership", "Communication skills", "Team collaboration"]
            }
        )
        
        # Validate response
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        
        # Validate mock call
        mock_get_job_by_id.assert_called_once_with(mock_job.job_id)
        mock_update_job.assert_called_once()

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    def test_update_job_not_found(self, mock_get_job_by_id):
        """Test updating a non-existent job"""
        # Set mock return value
        mock_get_job_by_id.return_value = None
        
        # Send request
        response = client.put(
            "/api/v1/job/nonexistent",
            json={
                "job_title": "Senior Frontend Developer"
            }
        )
        
        # Validate response
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "404"
        assert "Job not found" in data["message"]
        
        # Validate mock call
        mock_get_job_by_id.assert_called_once_with("nonexistent")

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    @patch("api.repositories.job_repository.JobRepository.delete_job")
    def test_delete_job(self, mock_delete_job, mock_get_job_by_id, mock_job):
        """Test deleting a job"""
        # Set mock return value
        mock_get_job_by_id.return_value = mock_job  # Check if the job exists first
        mock_delete_job.return_value = True
        
        # Send request
        response = client.delete(f"/api/v1/job/{mock_job.job_id}")
        
        # Validate response
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["deleted"] is True
        
        # Validate mock call
        mock_get_job_by_id.assert_called_once_with(mock_job.job_id)
        mock_delete_job.assert_called_once_with(mock_job.job_id)

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    def test_delete_job_not_found(self, mock_get_job_by_id):
        """Test deleting a non-existent job"""
        # Set mock return value - Job does not exist
        mock_get_job_by_id.return_value = None
        
        # Send request
        response = client.delete("/api/v1/job/nonexistent")
        
        # Validate response
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "404"
        assert "Job not found" in data["message"]
        
        # Validate mock call
        mock_get_job_by_id.assert_called_once_with("nonexistent") 