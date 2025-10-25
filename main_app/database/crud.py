from sqlalchemy import select, update, desc, func
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from asyncio import sleep
from aiogram.exceptions import TelegramForbiddenError

from main_app.core.bot_config import bot
from main_app.core.logger import logger
from main_app.database.session import async_session_maker
from main_app.core.app_config import created_at_irkutsk_tz
from main_app.database.models import User, Post


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


async def search_all_users():
    """ Поиск всех пользователей в таблице User в БД """
    async with async_session_maker() as session:
        users_query = select(User)
        users_result = await session.execute(users_query)
        users = users_result.scalars().all()
        if len(users) > 0:
            return users


async def search_all_posts():
    """ Поиск всех постов в таблице Post в БД """
    async with async_session_maker() as session:
        posts_query = select(Post)
        posts_result = await session.execute(posts_query)
        posts = posts_result.scalars().all()
        if len(posts) > 0:
            return posts


async def update_post_is_sent(post_id: int):
    """ Отмечаем пост как отправленный """
    async with async_session_maker() as session:
        await session.execute(update(Post).where(Post.id == post_id).values(is_sent=True))
        await session.commit()
