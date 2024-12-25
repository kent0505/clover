from fastapi                import FastAPI
from fastapi.staticfiles    import StaticFiles
from aiogram                import Bot, Dispatcher
from contextlib             import asynccontextmanager
from dotenv                 import load_dotenv

from src.database.base      import Base
from src.database.db_helper import db_helper
from src.routers.home       import router as home_router
from src.handlers           import router

import os
import logging
import asyncio

async def start_bot():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    logging.info("Starting Telegram bot")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logging.info("Telegram bot stopped")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()
    logging.info("STARTUP")
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    bot_task = asyncio.create_task(start_bot())
    yield
    # shutdown
    logging.info("SHUTDOWN")
    bot_task.cancel()
    await db_helper.dispose()

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.mount(app=StaticFiles(directory="static"),    path="/static")
app.mount(app=StaticFiles(directory="templates"), path="/templates")

app.include_router(home_router, include_in_schema=False)
# app.include_router(parser_router, prefix="/api/v1/parser", tags=["Parser"])

# venv\Scripts\activate or source venv/bin/activate
# pip install -r requirements.txt
# uvicorn src.main:app --reload
# alembic revision --autogenerate -m ""
# alembic upgrade head
