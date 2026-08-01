import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from bot.config import Settings
from bot.handlers import get_routers
from bot.db import engine


async def near_birthday_mess(bot: Bot) -> None:
    while True:
        temp = engine.check_birthdays()
        for user in temp:
            await bot.send_message(chat_id=user[0], text="У кого-то из твоих близких скоро день рождения. Напиши /check чтобы узнать у кого именно!!!")

        await asyncio.sleep(86400)



async def main():
    settings = Settings()

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=AiohttpSession(proxy=settings.PROXY)
    )

    dp = Dispatcher()
    dp.include_routers(*get_routers())

    bd_update_birthdays = asyncio.create_task(engine.update_birthdays())
    near_birthday = asyncio.create_task(near_birthday_mess(bot))
    polling = asyncio.create_task(dp.start_polling(bot))

    try:
        await near_birthday
        await bd_update_birthdays
        await polling
    finally:
        print("Бот закончил свою работу")



if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    asyncio.run(main())
