import sqlite3
from bot.db.entities import User, Birthday

class Engine:

    db: str

    def create_tables(self) -> None:
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_tg TEXT)""")
        
            cur.execute("""CREATE TABLE IF NOT EXISTS birthdays(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            bd_us_id INTEGER,
            FOREIGN KEY (bd_us_id) REFERENCES user(id)            
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )""")

            conn.commit()

    def insert_user(self, user: User) -> None:
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO users (user_tg)
            VALUES (?)
            """, (user.user_tg, ))
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

