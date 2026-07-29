import datetime as dt


class User:
    user_tg: str

class Birthday:
    def __init__(self, name, date, bd_us_id):
        self.name = name
        self.date = date
        self.bd_us_id = bd_us_id

    def get_date(self):
        return self.date

    def check_actuality(self):
        return self.date < dt.date.today()


