from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from typing import List
from fastapi_users import FastAPIUsers
import fastapi_users
from src.auth.manager import get_user_manager
from src.auth.auth import auth_backand
from src.auth.schemas import UserCreate, UserRead

from src.image.router import router as image_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="diving app")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    id: int
    role: str
    name: str

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backand]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backand),
    prefix="/auth/jwt",
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=['auth'],
)

app.include_router(image_router)
