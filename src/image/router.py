from fastapi import FastAPI, UploadFile
import os

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.path import root_dir

router = APIRouter(
  prefix="/images",
  tags=["Image"]
)

@router.get("/")
async def get_image_by_id(id: int):
  test = os.getcwd('C:\\fakepath\\Select.jpg')
  return f"new image here {id}"

class Item(BaseModel):
    image: UploadFile

@router.post("/")
async def create_item(file: UploadFile):
    new_dir = os.path.join(root_dir, 'assets');

    file_path = os.path.join(new_dir, file.filename)

    if not os.path.exists(new_dir):
       os.mkdir(new_dir)

    with open(file_path, "wb") as f:
        f.write(await file.read())
       
    return {"message": "Item created successfully"}