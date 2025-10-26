import pytz

from datetime import datetime
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    bot_token: str
    admin_id: int
    database_url: PostgresDsn
    list_admin_id: list

    class Config:
        env_file = ".env"


settings = Settings()

created_at_irkutsk_tz = datetime.now(pytz.timezone("Asia/Irkutsk"))

TELEGRAM_MESSAGE_LIMIT = 4096

DELETE_AFTER_SECONDS = 60  # удалить через 1 час
