import pytz

from datetime import datetime
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    bot_token: str
    admin_id: int
    database_url: PostgresDsn

    class Config:
        env_file = ".env"


settings = Settings()

created_at_irkutsk_tz = datetime.now(pytz.timezone("Asia/Irkutsk"))
