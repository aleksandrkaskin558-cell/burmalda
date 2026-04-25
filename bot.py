"""
bot.py — «Мозг» (Backend): Telegram-бот на Aiogram 3.x.
Отвечает за общение с пользователем в мессенджере
и открытие Mini App через WebAppInfo.
"""

import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

# URL Mini App (подставь свой адрес после деплоя)
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-url.com")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    """Обработчик команды /start — отправляет клавиатуру с кнопкой Mini App."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Открыть приложение",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "Добро пожаловать в Space Shop! 🚀\nНажмите кнопку ниже, чтобы открыть магазин.",
        reply_markup=keyboard,
    )


async def main() -> None:
    """Асинхронный запуск бота."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
