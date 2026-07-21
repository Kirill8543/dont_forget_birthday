import datetime as dt

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.db.entities import Birthday, User
from bot.db import engine
from bot.filters import BirthdayDiffFilter

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(
        message: Message,
        ) -> None:
    user = User()
    user.user_tg = message.from_user.id
    engine.insert_user(user)

    await message.answer("Хай, я бот Абобус и я помогу тебе не забыть о др, пук. Чтобы добавить пиши так: имя_фамилия день месяц")



@router.message(Command('check'))
async def get_birthdays(
        message: Message
         ) -> None:
    try:
        us_id = engine.get_user_id(message.from_user.id)
        birthdays = engine.select_birthdays(us_id)
        s = ""
        for item in birthdays:
            s += item[1] + ', ' + \
                 str(dt.date.fromisoformat(item[2]) - dt.date.today()) + "\n"
        await message.answer(s)

    except Exception:
        await message.answer("Соси")



@router.message(F.text)
async def add_birthday(
        message: Message,
        ) -> None:
    # try:
    name, day, month = message.text.split()

    if dt.date(year=dt.date.today().year, month=int(month), day=int(day)) < dt.date.today():
        date = dt.date(year=dt.date.today().year + 1, month=int(month), day=int(day))
    else:
        date = dt.date(year=dt.date.today().year, month=int(month), day=int(day))

    birthday = Birthday(name=name, date=date, bd_us_id=engine.get_user_id(message.from_user.id))
    birthday.get_date()
    engine.insert_birthday(birthday)

    # except Exception:
    #     await message.answer("Еба, ты хуйню высрал. Давай по-новой, Миша, всё хуйня")

    # else:
    await message.answer("Все день рождения добавлен и слит доксерам! (шутка)")


@router.message(BirthdayDiffFilter(7))
async def remind_birthday(message: Message) -> None:
    await message.answer("У одного из ваших близких скоро день рождения, чтобы узнать у кого, выполните команду /check")