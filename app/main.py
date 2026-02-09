import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from app.config import BOT_TOKEN, BASE_URL, WEBHOOK_PATH
from app.bot import handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

dp.message.register(handlers.start_cmd, Command("start"))
dp.message.register(handlers.help_cmd, Command("help"))
dp.message.register(handlers.reset_cmd, Command("reset"))
dp.message.register(handlers.image_handler, lambda m: m.photo)
dp.message.register(handlers.text_handler)

@app.on_event("startup")
async def on_startup():
    webhook_url = f"{BASE_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url)
    logging.info(f"Webhook set: {webhook_url}")

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    update = await request.json()
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}

@app.get("/health")
def health():
    return {"status": "ok"}
