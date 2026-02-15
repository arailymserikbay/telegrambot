import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from app.config import BOT_TOKEN, BASE_URL, WEBHOOK_PATH
from app.bot import handlers

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")
if not BASE_URL:
    raise RuntimeError("BASE_URL is missing")
if not WEBHOOK_PATH:
    raise RuntimeError("WEBHOOK_PATH is missing")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

dp.message.register(handlers.start_cmd, Command("start"))
dp.message.register(handlers.help_cmd, Command("help"))
dp.message.register(handlers.reset_cmd, Command("reset"))

dp.message.register(handlers.image_handler, F.photo)
dp.message.register(handlers.text_handler, F.text)

@app.on_event("startup")
async def on_startup():
    webhook_url = f"{BASE_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url)
    logging.info(f"✅ Webhook set: {webhook_url}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook(drop_pending_updates=True)

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    update = await request.json()
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}

@app.get("/health")
def health():
    return {"status": "ok"}
