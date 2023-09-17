from fastapi import UploadFile
from models import Image
from sqlalchemy.ext.asyncio import AsyncSession
import os

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.database import get_async_session
from sqlalchemy import insert

router = APIRouter(
    prefix="/images",
    tags=["Image"]
)


@router.get("/")
async def get_image_by_id(id: int):
    return f"new image here {id}"


class Item(BaseModel):
    image: UploadFile


@router.post("/")
async def create_item(file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    data = Image(path='John Doe', name="user", description="new Test")

    stmt = insert(Image).values(path='John Doe', name="user", description="new Test")

    await session.execute(stmt)
    await session.commit()

    print(session, 'sessing')

    # new_dir = os.path.join(root_dir, 'assets');

    # file_path = os.path.join(new_dir, file.filename)

    # if not os.path.exists(new_dir):
    #    os.mkdir(new_dir)

    # with open(file_path, "wb") as f:
    #     f.write(await file.read())

    return {"message": "Item created successfully"}
