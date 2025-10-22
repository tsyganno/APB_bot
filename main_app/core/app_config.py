from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    admin_id: int

    class Config:
        env_file = ".env"


settings = Settings()
