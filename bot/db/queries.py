import sqlite3
from bot.db.entities import User, Birthday
import asyncio
import datetime as dt

class Engine:

    db: str

    def create_tables(self) -> None:
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_tg TEXT,
            chat_id INTEGER)""")
        
            cur.execute("""CREATE TABLE IF NOT EXISTS birthdays(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date DATE,
            bd_us_id INTEGER,
            FOREIGN KEY (bd_us_id) REFERENCES user(id)            
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )""")

            conn.commit()
    def create_trigger(self) -> None:
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            # Этот триггер не будет работать ибо нет триггера SELECT (((
            # Надо сделать TRIGGER на вставку, чтобы автоматом дату двигал при вставке, но это не решает фулл траблс,
            # так что вытаскиваем логику из engine в Birthday... или не

            # cur.execute("""CREATE TRIGGER before_select_year BEFORE SELECT
            #                 ON birthdays FOR EACH ROW
            #                 BEGIN
            #                     UPDATE birthdays
            #                     SET date = DATE(OLD.date, '+1 year')
            #                     WHERE date < ?
            #                 END;""", (dt.date.today(), ))
            conn.commit()

    def insert_user(self, user: User) -> None:
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO users (user_tg, chat_id)
            VALUES (?, ?)
            """, (user.user_tg, user.chat_id))
            conn.commit()

    def insert_birthday(self, birthday: Birthday) -> None:
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO birthdays (name, date, bd_us_id)
            VALUES (?, ?, ?)
            """, (birthday.name, birthday.date, birthday.bd_us_id))
            conn.commit()

    def select_birthdays(self, user_tg):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()

            return cur.execute(f"""
                                SELECT *
                                FROM birthdays
                                WHERE bd_us_id = ?
                                ORDER BY date, id""", (user_tg, )).fetchall()
    
    def get_user_id(self, user_tg):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            return cur.execute(f"""
                                SELECT id
                                FROM users
                                WHERE user_tg = ?
                                """, (user_tg, )).fetchone()[0]

    async def update_birthdays(self):
        while True:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()

                temp = cur.execute("""SELECT * 
                                    FROM birthdays 
                                    ORDER BY date, id""").fetchone()

                birthday = None

                if temp:
                    birthday = Birthday(name=temp[1], date=dt.date.fromisoformat(temp[2]), bd_us_id=temp[3])

                if birthday and birthday.check_actuality():
                    cur.execute("""UPDATE birthdays 
                                    SET date = DATE(date, '+1 year')
                                    WHERE date < DATE('now');""")

                conn.commit()
            await asyncio.sleep(86400)

    def check_birthdays(self) -> list[tuple]:
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()

            temp = cur.execute("""SELECT chat_id
                            FROM users
                            JOIN birthdays ON users.id = birthdays.bd_us_id
                            WHERE DATE(birthdays.date, '-7 day') <= DATE('now')
                            GROUP BY users.chat_id""").fetchall()

            return temp