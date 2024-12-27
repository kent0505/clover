from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy             import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing                 import Literal

from src.database.db_helper import db_helper
from src.database.base      import User

router = APIRouter()

@router.get("/all")
async def get_users(db: AsyncSession = Depends(db_helper.get_db)):
    users = await db.scalars(select(User))
    return {
        "users": [
            {
                "id":     user.id,
                "uid":    user.uid,
                "coins":  user.coins,
                "friend": user.friend,
                "avatar": user.avatar,
                "login":  user.login,
                "status": user.status,
            } 
            for user in users
        ]
    }

@router.post("/ban")
async def ban_user(
    uid:    int, 
    status: Literal["active", "ban"],
    db:     AsyncSession = Depends(db_helper.get_db),
):
    user = await db.scalar(select(User).filter(User.uid == uid))
    if user:
        user.status = status
        await db.commit()
        return {"message": status}
    raise HTTPException(404, "user id not found")
