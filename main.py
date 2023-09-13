from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from typing import List
from fastapi_users import FastAPIUsers
import fastapi_users
from src.auth.manager import get_user_manager
from src.auth.auth import auth_backand

from src.auth.schemas import UserCreate, UserRead

app = FastAPI(title="diving app")

fake_users = [
    {"id": 1, "role": "user", "name": "test"},
    {"id": 2, "role": "user", "name": "test"},
    {"id": 3, "role": "user", "name": "test"},
    {"id": 4, "role": "user", "name": "test"},
]


class User(BaseModel):
    id: int
    role: str
    name: str


@app.get("/users/{user_id}", response_model=List[User])
def get_hello(user_id: int):
    user = [user["name"] for user in fake_users if user.get("id") == user_id]
    return fake_users


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123},
]


@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


fake_users2 = [
    {"id": 1, "name": "ana", "female": "test"},
    {"id": 2, "name": "ana"},
    {"id": 3, "name": "ana"},
    {"id": 4, "name": "ana"},
]


@app.post("/users/{user_id}")
def post_user(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user["name"] = new_name

    print(current_user, "user")
    return {"status": 200, "data": current_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    price: float = Field(ge=0)
    side: str


@app.post("/traids")
def add_traids(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}

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

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, Anonim"
