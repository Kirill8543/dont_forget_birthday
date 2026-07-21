from bot.db.queries import Engine

db = "db/birthdays.db"

engine = Engine()
engine.db = db


def main():
    engine.create_tables()


if __name__ == '__main__':
    main()

