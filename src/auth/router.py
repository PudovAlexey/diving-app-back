import secrets
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from pydantic import BaseModel
from src.auth.manager import get_user_manager
from src.auth.auth import auth_backand
from src.auth.schemas import UserCreate, UserRead
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
from src.database import get_async_session
from src.users.queries import user_by_id_query
from src.auth.models import User
from src.mailer.main import send_email
from src.redis.main import redis_client
from src.INTL import INTL
from src.INTL.request_status import Statuses
from src.auth.schemas import UserModel

JWT_router = APIRouter(
    prefix="/auth/jwt",
    tags=["auth"]
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


fastapi_users = FastAPIUsers[UserModel, int](
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
        send_email(to=user_data["data"].email, subject=INTL["AUTH"]["INVITE"]["SUBJECT"],
                   message_text=INTL["AUTH"]["INVITE"]["MESSAGE_TEXT"](f"http://localhost:8000/auth/user_confirm/{secret_key}"))
        return {
            "message": "Приглашение успешно отправлено, пожалуйста проверьте свой почтовый ящик",
            "status": Statuses.SUCCESS
        }
    except:
        return {
            "message": "Не удалось отправить приглашение, пожалуйста повторите позднее",
            "status": Statuses.ERROR
        }


@router.get("/user_confirm/{secret_key}")
async def user_confirm(secret_key: str, session: AsyncSession = Depends(get_async_session)):
    try:
        user_id = redis_client.get(f'request_hash:{secret_key}')
        if (user_id == None):
            return {
                "message": "Приглашение не найдено",
                "status": Statuses.ERROR
            }
        stmt = update(User).where(User.id == int(user_id)).values(is_verified=True)
        await session.execute(stmt)
        await session.commit()
        return {
            "message": 'Пользователь подтвержден',
            "status": Statuses.SUCCESS
        }
    except:
        return {
            "message": "Не удалось подтвердить профиль, попробуйте поздеее",
            "status": Statuses.ERROR
        }
    # return {"done": True}
