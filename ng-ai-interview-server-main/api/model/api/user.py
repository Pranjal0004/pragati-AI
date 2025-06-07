from datetime import datetime
from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    """Create user request model"""
    user_name: str
    password: str
    staff_id: str | None = None
    email: EmailStr
    role: int = 1  # Default to interviewee

class UpdateUserRequest(BaseModel):
    """Update user request model"""
    user_name: str | None = None
    password: str | None = None
    staff_id: str | None = None
    email: EmailStr | None = None
    status: int | None = None
    role: int | None = None

class UserResponse(BaseModel):
    """User response model"""
    user_id: str
    user_name: str
    staff_id: str | None
    email: str
    status: int
    role: int
    create_date: datetime 