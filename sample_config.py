import os
import typing

class Config:
    # get a token from @BotFather
    TG_BOT_TOKEN: str = os.environ.get("TG_BOT_TOKEN", "")
    # check if TG_BOT_TOKEN is not an empty string
    if not TG_BOT_TOKEN:
        raise ValueError("TG_BOT_TOKEN environment variable is not set")

    # The Telegram API things
    APP_ID: int = int(os.environ.get("APP_ID", 12345))
    # check if APP_ID is a valid integer
    if not isinstance(APP_ID, int):
        raise ValueError("APP_ID environment variable is not a valid integer")

    API_HASH: str = os.environ.get("API_HASH", "")
    # Update channel for Force Subscribe
    UPDATE_CHANNEL: str = os.environ.get("UPDATE_CHANNEL", "")
    # log channel
    #LOG_CHANNEL: str = os.environ.get("LOG_CHANNEL", "")
    # Get these values from my.telegram.org
    CHAT_ID: str = os.environ.get("CHAT_ID", "")
    # Array to store users who are authorized to use the bot
    AUTH_USERS: typing.Set[int] = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    # check if AUTH_USERS is not an empty set
    if not AUTH_USERS:
        raise ValueError("AUTH_USERS environment variable is not set")

    BANNED_USERS: typing.List[int] = []
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION: str = "./DOWNLOADS"
    # Telegram maximum file upload size
    MAX_FILE_SIZE: int = 50000000
    TG_MAX_FILE_SIZE: int = 2097152000
    FREE_USER_MAX_FILE_SIZE: int
