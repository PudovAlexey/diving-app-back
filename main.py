from fastapi import Depends, FastAPI

from src.auth.schemas import UserCreate, UserRead
from fastapi.middleware.cors import CORSMiddleware


from src.image.router import router as image_router
from src.users.router import router as user_router
from src.auth.router import router as auth_router, JWT_router as jwt_router


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
