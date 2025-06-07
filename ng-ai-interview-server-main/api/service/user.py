import uuid
import bcrypt
from api.model.api.user import CreateUserRequest, UpdateUserRequest, UserResponse
from api.model.db.user import User
from api.repositories.user_repository import UserRepository
from api.utils.log_decorator import log
from typing import List
from api.exceptions.api_error import ValidationError, NotFoundError, DuplicateError

class UserService:
    def __init__(self):
        self.repository = UserRepository()
    
    @log
    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        """Create a new user"""
        # Check if email exists
        existing_user = await self.repository.get_user_by_email(request.email)
        if existing_user:
            raise DuplicateError("Email already registered")
        
        # Check if staff ID exists
        existing_user = await self.repository.get_user_by_staff_id(request.staff_id)
        if existing_user:
            raise DuplicateError("Staff ID already registered")

        # Hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(request.password.encode(), salt)
        
        # Create user document
        user = User(
            user_id=str(uuid.uuid4()),
            user_name=request.user_name,
            password=hashed.decode(),
            staff_id=request.staff_id,
            email=request.email,
            role=request.role
        )
        
        # Save to database
        user = await self.repository.create_user(user)
        
        return self._to_response(user)
    
    @log
    async def get_user(self, user_id: str) -> UserResponse:
        """Get user by ID"""
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        return self._to_response(user)
    
    @log
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get users with pagination"""
        users = await self.repository.get_users(skip, limit)
        return [self._to_response(user) for user in users]
    
    @log
    async def update_user(self, user_id: str, request: UpdateUserRequest) -> UserResponse:
        """Update user"""
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        # Update fields if provided
        if request.user_name:
            user.user_name = request.user_name
        if request.password:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(request.password.encode(), salt)
            user.password = hashed.decode()
        if request.staff_id:
            user.staff_id = request.staff_id
        if request.email:
            user.email = request.email
        if request.status is not None:
            user.status = request.status
        if request.role is not None:
            user.role = request.role
        
        user = await self.repository.update_user(user)
        return self._to_response(user)
    
    @log
    async def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        return await self.repository.delete_user(user_id)
    
    def _to_response(self, user: User) -> UserResponse:
        """Convert User document to UserResponse"""
        return UserResponse(
            user_id=user.user_id,
            user_name=user.user_name,
            staff_id=user.staff_id,
            email=user.email,
            status=user.status,
            role=user.role,
            create_date=user.create_date
        ) 