from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from sqlalchemy import select
from src.database import get_async_session
async def user_by_id_query(id: int, session):
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    return {
        "status": "success",
        "data": result.scalars().one(),
        "details": None
    }

