import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from aiogram.filters import Command
from handlers import user

TOKEN = "7988253030:AAFp18gIfweRt3jpvNAiZhFOYlojjXA-NS4"

async def main():

    TOKEN = "7988253030:AAFp18gIfweRt3jpvNAiZhFOYlojjXA-NS4"             
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")