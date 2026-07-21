import asyncio

from aiogram import Bot, Dispatcher

from bot.start.router import router as start_router

from .config import API_TOKEN


bot = Bot(token=API_TOKEN)


dp = Dispatcher()

dp.include_router(start_router)


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())