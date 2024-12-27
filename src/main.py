from fastapi                import FastAPI
from fastapi.staticfiles    import StaticFiles
from aiogram                import Bot, Dispatcher
from contextlib             import asynccontextmanager
from dotenv                 import load_dotenv

from src.database.base      import Base
from src.database.db_helper import db_helper
from src.handlers           import router
from src.routers.home       import router as home_router
from src.routers.admin      import router as admin_router
from src.routers.user       import router as user_router
from src.routers.avatar     import router as avatar_router
from src.routers.task       import router as task_router

import os
import logging
import asyncio

async def start_bot():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    bot_task = asyncio.create_task(start_bot())
    yield
    bot_task.cancel()
    await db_helper.dispose()

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.mount(app=StaticFiles(directory="static"),    path="/static")
app.mount(app=StaticFiles(directory="templates"), path="/templates")

app.include_router(home_router, include_in_schema=False)
app.include_router(admin_router,  prefix="/api/v1/admin",  tags=["Admin"])
app.include_router(user_router,   prefix="/api/v1/user",   tags=["User"])
app.include_router(avatar_router, prefix="/api/v1/avatar", tags=["Avatar"])
app.include_router(task_router,   prefix="/api/v1/task",   tags=["Task"])

# venv\Scripts\activate or source venv/bin/activate
# pip install -r requirements.txt
# uvicorn src.main:app --reload
# alembic revision --autogenerate -m ""
# alembic upgrade head
