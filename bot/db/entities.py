import datetime as dt


class User:
    def __init__(self, user_tg, chat_id):
        self.user_tg = user_tg
        self.chat_id = chat_id

class Birthday:
    def __init__(self, name, date, bd_us_id):
        self.name = name
        self.date = date
        self.bd_us_id = bd_us_id

    def get_date(self):
        return self.date

    def check_actuality(self):
        return self.date < dt.date.today()


