import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers import user

async def main():
    TOKEN = os.getenv("BOT_TOKEN")  # берём токен из переменных окружения

    if not TOKEN:
        raise ValueError("BOT_TOKEN not found in environment variables")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(user)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
