import datetime as dt


class User:
    user_tg: str

class Birthday:
    def __init__(self, name, date, bd_us_id):
        self.name = name
        self.bd_us_id = bd_us_id
        self.date = date

    def get_date(self):
        return self.date

    def get_timediff(self):
        return self.date - dt.date.today()

