import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from aiogram.filters import Command
from handlers import user

TOKEN = ""

async def main():

    TOKEN = ""             
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:

        print("Bot stopped")
