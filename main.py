from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from src.auth.router import JWT_router as jwt_router
from src.auth.router import router as auth_router
from src.image.router import router as image_router
from src.users.router import router as user_router

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
app.include_router(jwt_router)
app.include_router(auth_router)
app.include_router(image_router)
app.include_router(user_router)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
