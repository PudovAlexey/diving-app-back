from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.database import get_async_session
from sqlalchemy import insert
router = APIRouter(
    prefix="/userInfo",
    tags=["UserInfo"]
)