from fastapi                import APIRouter, HTTPException, UploadFile, Depends
from sqlalchemy             import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_helper import db_helper
from src.database.base      import Avatar

import os
import time

router = APIRouter()

@router.get("/")
async def get_avatars(db: AsyncSession = Depends(db_helper.get_db)):
    avatars = await db.scalars(select(Avatar))
    return {
        "avatars": [
            {
                "id":    avatar.id,
                "title": avatar.title,
            } 
            for avatar in avatars
        ]
    }

@router.post("/")
async def add_avatar(
    file: UploadFile, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    unique_name = f"{int(time.time()) }.{str(file.filename).split('.')[-1]}" # 1706520261.png
    file_name   = os.path.join("static", unique_name)
    with open(file_name, "wb") as image_file:
        image_file.write(file.file.read())

    db.add(Avatar(title=unique_name))
    await db.commit()
    return {"message": "avatar added"}

@router.delete("/")
async def delete_avatar(
    id: int,
    db: AsyncSession = Depends(db_helper.get_db)
):
    avatar = await db.scalar(select(Avatar).filter(Avatar.id == id))
    if avatar:
        await db.delete(avatar)
        await db.commit()
        return {"message": "avatar deleted"}
    raise HTTPException(404, "avatar id not found")