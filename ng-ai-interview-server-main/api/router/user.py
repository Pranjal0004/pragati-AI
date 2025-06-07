from fastapi import APIRouter, Query
from api.model.api.user import CreateUserRequest, UpdateUserRequest, UserResponse
from api.model.api.base import Response
from api.service.user import UserService

router = APIRouter(prefix="/user", tags=["user"])
service = UserService()

@router.post("")
async def create_user(request: CreateUserRequest) -> Response[UserResponse]:
    """Create a new user"""
    user = await service.create_user(request)
    return Response(data=user)

@router.get("/{user_id}")
async def get_user(user_id: str) -> Response[UserResponse]:
    """Get user by ID"""
    user = await service.get_user(user_id)
    return Response(data=user)

@router.get("")
async def get_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100)
) -> Response[list[UserResponse]]:
    """Get users with pagination"""
    users = await service.get_users(skip, limit)
    return Response(data=users)

@router.put("/{user_id}")
async def update_user(user_id: str, request: UpdateUserRequest) -> Response[UserResponse]:
    """Update user"""
    user = await service.update_user(user_id, request)
    return Response(data=user)

@router.delete("/{user_id}")
async def delete_user(user_id: str) -> Response:
    """Delete user"""
    result = await service.delete_user(user_id)
    return Response(data={"deleted": result}) 