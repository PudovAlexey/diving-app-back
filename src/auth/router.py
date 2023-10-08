import secrets
import redis
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from pydantic import BaseModel
from src.auth.manager import get_user_manager
from src.auth.auth import auth_backand
from src.auth.schemas import UserCreate, UserRead
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, update, insert
from src.database import get_async_session
from src.users.queries import user_by_id_query
from src.auth.models import User as UserModel
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from src.mailer.main import send_email
from src.database import Base

redis_client = redis.Redis(host='localhost', port=6379)

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

@router.post("/request_invite/{user_id}")
async def request_invite(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        user_data = await user_by_id_query(user_id, session)
        secret_key = secrets.token_hex(16)
        redis_client.set(f'request_hash:{secret_key}', user_id)
        redis_client.expire(f'request_hash:{secret_key}', 5000)
        send_email(to=user_data["data"].email, subject="Код авторизации",
                   message_text=f'Перейдите по ссылке для подтверждения своего email адреса http://localhost:8000/auth/user_confirm/{secret_key}')
        return secret_key
    except ValueError:
        return ValueError

@router.get("/user_confirm/{secret_key}")
async def user_confirm(secret_key: str, session: AsyncSession = Depends(get_async_session)):
    user_id = redis_client.get(f'request_hash:{secret_key}')
    # user = await session.get(User, int(user_id))
    stmt = update(UserModel).where(UserModel.id == int(user_id)).values(is_verified=True)
    await session.execute(stmt)
    await session.commit()
#     stmt = (
#     update(User.__table)
#     .where(User.id == int(user_id))
#     .values(is_verified=True)
# )
#     await session.execute(stmt)
#     # user = result.scalar();
#     # user.is_verified = True
#     await session.commit()
#     # await session.close()
    return {"done": True}