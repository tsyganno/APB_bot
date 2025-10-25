from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from main_app.core.bot_config import settings

# Создаем асинхронный движок
engine = create_async_engine(
    str(settings.database_url),
    echo=False,  # Включи True, если хочешь видеть SQL-запросы в логах
    future=True
)

# Сессия
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass
