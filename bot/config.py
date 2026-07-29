import tomllib


class Settings:
    BOT_TOKEN: str
    PROXY: str
    IP: str
    LOGIN: str
    PASS: str

    def __init__(self):
        with open("settings.toml", "rb") as f:
            config = tomllib.load(f)

            self.BOT_TOKEN = config["bot"]["token"]
            self.PROXY = config["proxy"]["url"]


