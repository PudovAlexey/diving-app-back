from fastapi import APIRouter, Depends
from sqlalchemy import select
from pydantic import BaseModel
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.userInfo.models import UserInfo
from sqlalchemy.orm import joinedload
from src.mailer.main import send_email
from .queries import user_by_id_query

router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.get("/")
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User).join(User.user_info).options(joinedload(User.user_info))
    result = await session.execute(query)
    data = result.scalars().all()
    return {
        "status": "success",
        "data": data,
        "details": None
    }


@router.get("/{id}")
async def get_user_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    return await user_by_id_query(id, session)
