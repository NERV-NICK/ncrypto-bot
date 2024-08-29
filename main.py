from fastapi import Request
import uvicorn

from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, Message

from bot.handlers import router
from bot.database.models import async_main

from app.app import app

import os
import dotenv

dotenv.load_dotenv()


bot = Bot(token=f"{os.getenv('TOKEN')}")
dp = Dispatcher()
dp.include_router(router)


WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{os.getenv('URL')}{WEBHOOK_PATH}"


@app.on_event("startup")
async def startup() -> None:
    await bot.delete_webhook()
    await bot.set_webhook(url=f"{WEBHOOK_URL}")
    await async_main()


@app.post("/webhook")
async def update(request: Request) -> None:
    data = await request.json()
    update = Update.model_validate(await request.json(), context={"bot": bot})
    if "message" in data:
        message = Message(**data["message"])
        await dp._process_update(bot, update)
    return {"ok": True}


if __name__ == '__main__':
    uvicorn.run(app)