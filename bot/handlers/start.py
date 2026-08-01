import datetime as dt

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


from bot.db.entities import Birthday, User
from bot.db import engine


router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(
        message: Message,
        ) -> None:
    user = User(user_tg=message.from_user.id, chat_id=message.chat.id)
    engine.insert_user(user)

    await message.answer("Хай, я бот Абобус и я помогу тебе не забыть о др, пук. Чтобы добавить др пиши так: имя_фамилия день месяц. После добавления всех ДР напиши /check, чтобы узнать когда ДР твоих близких")


# для этого роутера надо написать Filter или Middleware для проверки пользователя
@router.message(Command('check'))
async def get_birthdays(
        message: Message
         ) -> None:
    try:
        us_id = engine.get_user_id(message.from_user.id)

        birthdays = engine.select_birthdays(us_id)
        s = ""
        for item in birthdays:
            days = (dt.date.fromisoformat(item[2]) - dt.date.today()).days
            if days % 10 == 1:
                s += item[1] + " - " + str(days) + " день" + "\n"
            elif str(days % 10) in "234":
                s += item[1] + " - " + str(days) + " дня" + "\n"
            else:
                s += item[1] + " - " + str(days) + " дней" + "\n"


        await message.answer(s)

    except Exception:
        await message.answer("Для начала общения с ботом напишите команду /start")

@router.message(F.text)
async def add_birthday(
        message: Message,
        ) -> None:
    try:
        name, day, month = message.text.split()

        if dt.date(year=dt.date.today().year, month=int(month), day=int(day)) < dt.date.today():
            date = dt.date(year=dt.date.today().year + 1, month=int(month), day=int(day))
        else:
            date = dt.date(year=dt.date.today().year, month=int(month), day=int(day))

        birthday = Birthday(name=name,
                            date=date,
                            bd_us_id=engine.get_user_id(message.from_user.id))

        birthday.get_date()
        engine.insert_birthday(birthday)

    except Exception:
        await message.answer("Ошибка ввода сообщения. Чтобы добавить ДР пишите в таком формате: имя_фамилия день месяц!")

    else:
        await message.answer("Всё день рождения добавлен и слит доксерам! (шутка)")






