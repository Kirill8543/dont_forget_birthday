import asyncio

from aiogram import Bot, Dispatcher
from bot.config import Settings
from bot.handlers import get_routers
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main():
    settings = Settings()

    bot = Bot(
        token=settings.BOT_TOKEN
    )

    dp = Dispatcher()

    dp.include_routers(*get_routers())

    try:
        await dp.start_polling(bot)
    finally:
        print("Соси я оффнул бота хыхыхыхых")



if __name__ == '__main__':
    asyncio.run(main())
