from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy             import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic               import BaseModel

from src.database.db_helper import db_helper
from src.database.base      import Task

router = APIRouter()

class _Body(BaseModel):
    id:       int = 0
    title:    str
    coins:    int
    diamonds: int

# @router.get("/", dependencies=[Depends(JWTBearer(role="user"))])
@router.get("/")
async def get_tasks(db: AsyncSession = Depends(db_helper.get_db)):
    tasks = await db.scalars(select(Task))
    return {
        "tasks": [
            {
                "id":       task.id,
                "title":    task.title,
                "coins":    task.coins,
                "diamonds": task.diamonds,
            } 
            for task in tasks
        ]
    }

@router.post("/")
async def add_task(
    body: _Body,
    db:   AsyncSession = Depends(db_helper.get_db)
):
    # if file.filename and str(file.content_type).startswith("image/"):
        # unique_name = f"{int(time.time()) }.{str(file.filename).split('.')[-1]}" # 1706520261.png
        # file_name   = os.path.join("static", unique_name)
        # with open(file_name, "wb") as image_file:
        #     image_file.write(file.file.read())

        db.add(Task(
            title=body.title,
            # image=unique_name,
            coins=body.coins,
            diamonds=body.diamonds,
        ))
        await db.commit()
        return {"message": "task added"}
    # raise HTTPException(400, "file error")

@router.put("/")
async def edit_task(
    body: _Body,
    db:   AsyncSession = Depends(db_helper.get_db)
):
    task = await db.scalar(select(Task).filter(Task.id == body.id))
    if task:
        # if file.filename and str(file.content_type).startswith("image/"):
            # os.remove(f"static/{task.image}")
            # unique_name = f"{int(time.time()) }.{str(file.filename).split('.')[-1]}" # 1706520261.png
            # file_name   = os.path.join("static", unique_name)
            # with open(file_name, "wb") as image_file:
            #     image_file.write(file.file.read())

            task.title    = body.title
            # task.image    = unique_name
            task.coins    = body.coins
            task.diamonds = body.diamonds
            await db.commit()
            return {"message": "task updated"}
        # raise HTTPException(400, "file error")
    raise HTTPException(404, "task id not found")

@router.delete("/")
async def delete_task(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    task = await db.scalar(select(Task).filter(Task.id == id))
    if task:
        await db.delete(task)
        await db.commit()
        return {"message": "task deleted"}
    raise HTTPException(404, "task id not found")

# ы
