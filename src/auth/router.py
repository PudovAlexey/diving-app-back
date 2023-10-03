from fastapi_users import FastAPIUsers
from pydantic import BaseModel
from src.auth.manager import get_user_manager
from src.auth.auth import auth_backand
from src.auth.schemas import UserCreate, UserRead
from fastapi import APIRouter

JWT_router = APIRouter(
    prefix="/auth/jwt",
    tags=["auth"]
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class User(BaseModel):
    id: int
    role: str
    name: str

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backand]
)

JWT_router.include_router(fastapi_users.get_auth_router(auth_backand))

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))