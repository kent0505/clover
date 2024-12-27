from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy             import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_helper import db_helper
from src.database.base      import User, Avatar

import time

router = APIRouter()

@router.get("/")
async def get_user(
    uid:    int, 
    friend: int = 0,
    db:     AsyncSession = Depends(db_helper.get_db),
):
    login: int = int(time.time())
    user = await db.scalar(select(User).filter(User.uid == uid))
    if user: 
        return {
            "code": 200,
            "user": {
                "uid":    user.uid,
                "coins":  user.coins,
                "friend": user.friend,
                "avatar": user.avatar,
                "login":  login,
                "status": user.status,
            }
        }
    else:
        bonus_coins = 0
        if friend == 0:
            db.add(User(
                uid=uid, 
                login=login
            ))
        else:
            friend_user = await db.scalar(select(User).filter(User.uid == friend))
            if friend_user:
                bonus_coins = 25000
                friend_user.coins += bonus_coins
                db.add(User(
                    uid=uid,
                    coins=bonus_coins,
                    friend=friend,
                    login=login,
                ))
            else:
                db.add(User(
                    uid=uid, 
                    login=login
                ))
        await db.commit()
        return {
            "code": 201,
            "user": {
                "uid":    uid,
                "coins":  bonus_coins,
                "friend": friend,
                "avatar": 1,
                "login":  login,
                "status": "active",
            }
        }

@router.post("/coins/")
async def add_coins(
    uid:   int,
    coins: int,
    db:    AsyncSession = Depends(db_helper.get_db),
):
    user = await db.scalar(select(User).filter(User.uid == uid))
    if user: 
        user.coins += coins
        await db.commit()
        return {"message": "coins added"}
    raise HTTPException(404, "user id not found")

@router.put("/avatar")
async def change_avatar(
    id:  int,
    uid: int, 
    db:  AsyncSession = Depends(db_helper.get_db)
):
    avatar = await db.scalar(select(Avatar).filter(Avatar.id == id))
    if avatar:
        user = await db.scalar(select(User).filter(User.uid == uid))
        if user:
            user.avatar = id
            await db.commit()
            return {"message": "avatar changed"}
        raise HTTPException(404, "user id not found")
    raise HTTPException(404, "avatar id not found")
