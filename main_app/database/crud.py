from sqlalchemy import select, update, desc, func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from asyncio import sleep
from aiogram.exceptions import TelegramForbiddenError

from main_app.core.bot_config import bot
from main_app.core.logger import logger
from main_app.database.session import async_session_maker
from main_app.core.app_config import created_at_irkutsk_tz
from main_app.database.models import User


async def save_user_to_db(user_data: dict, telegram_id: int, username: str):
    """ Запись пользователя в таблицу User в БД """
    async with async_session_maker() as session:
        user_query = select(User).where(User.telegram_id == telegram_id)
        user_result = await session.execute(user_query)
        user = user_result.scalars().first()

        if not user:
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                name=user_data["name"],
                created_at=created_at_irkutsk_tz,
            )
            session.add(new_user)
        else:
            await session.execute(
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(
                    username=username,
                    name=user_data["name"],
                    created_at=created_at_irkutsk_tz,
                )
            )

        await session.commit()
