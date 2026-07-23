import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from bot.config import Settings
from bot.handlers import get_routers
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.middlewares.middleware import SchedulerMiddleware


async def main():
    settings = Settings()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()

    bot = Bot(
        token=settings.BOT_TOKEN
    )

    dp = Dispatcher()

    dp.include_routers(*get_routers())
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )

    try:
        await dp.start_polling(bot)
    finally:
        print("Соси я оффнул бота хыхыхыхых")



if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    asyncio.run(main())
