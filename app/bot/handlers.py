import os
from aiogram import types, F
from app.bot.context import add_message, get_context, reset_context
from app.llm.ollama import ask_llm
from app.vision.blip import get_image_caption
from app.config import DATA_DIR, MAX_IMAGE_MB

async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Привет!\n"
        "Я AI-бот:\n"
        "• отвечаю на текст\n"
        "• анализирую изображения"
    )

async def help_cmd(message: types.Message):
    await message.answer(
        "/start — старт\n"
        "/help — помощь\n"
        "/reset — сброс контекста\n\n"
        "Отправь текст или изображение."
    )

async def reset_cmd(message: types.Message):
    reset_context(message.chat.id)
    await message.answer("🔄 Контекст сброшен.")

async def text_handler(message: types.Message):
    add_message(message.chat.id, "user", message.text)
    ctx = get_context(message.chat.id)

    answer = await ask_llm(list(ctx))
    add_message(message.chat.id, "assistant", answer)

    await message.answer(answer)

async def image_handler(message: types.Message):
    photo = message.photo[-1]
    size_mb = photo.file_size / (1024 * 1024)

    if size_mb > MAX_IMAGE_MB:
        await message.answer("❌ Изображение слишком большое.")
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    path = f"{DATA_DIR}/{photo.file_unique_id}.jpg"

    await message.bot.download(photo, destination=path)

    caption = await get_image_caption(path)
    user_text = message.caption or ""

    combined = f"Описание изображения: {caption}\n\nВопрос пользователя: {user_text}"

    add_message(message.chat.id, "user", combined)
    ctx = get_context(message.chat.id)

    answer = await ask_llm(list(ctx))
    add_message(message.chat.id, "assistant", answer)

    await message.answer(answer)
