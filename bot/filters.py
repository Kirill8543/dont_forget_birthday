import datetime as dt

from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.db import engine


class BirthdayDiffFilter(BaseFilter):
    def __init__(self, timediff: int):
        self.timediff = timediff

    async def __call__(self, message: Message) -> bool:
        us_id = engine.get_user_id(message.from_user.id)
        nearest_birthday = dt.date.fromisoformat(engine.select_birthdays(us_id)[0][2])
        return (nearest_birthday - dt.date.today()).days <= self.timediff

