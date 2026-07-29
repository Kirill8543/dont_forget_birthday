import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

from bot.config import Settings
from bot.handlers import get_routers
from bot.db import engine



async def main():
    settings = Settings()


    session = AiohttpSession(proxy=settings.PROXY)

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session
    )

    dp = Dispatcher()

    dp.include_routers(*get_routers())
    bd_update_birthdays = asyncio.create_task(engine.update_birthdays())
    polling = asyncio.create_task(dp.start_polling(bot))
    try:
        await bd_update_birthdays
        await polling
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
