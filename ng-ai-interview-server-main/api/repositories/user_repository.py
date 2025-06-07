from typing import Optional, List
from api.model.db.user import User
from api.utils.log_decorator import log

class UserRepository:
    @log
    async def create_user(self, user: User) -> User:
        """Create a new user"""
        return user.save()
    
    @log
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return User.objects(user_id=user_id).first()
    
    @log
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return User.objects(email=email).first()

    @log
    async def get_user_by_staff_id(self, staff_id: str) -> Optional[User]:
        """Get user by staff ID"""
        if staff_id is None or staff_id == "":
            return None
        return User.objects(staff_id=staff_id).first()

    @log
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users with pagination"""
        return User.objects().skip(skip).limit(limit).all()
    
    @log
    async def update_user(self, user: User) -> User:
        """Update user"""
        return user.save()
    
    @log
    async def delete_user(self, user_id: str) -> bool:
        """Delete user by ID"""
        result = User.objects(user_id=user_id).delete()
        return result > 0 