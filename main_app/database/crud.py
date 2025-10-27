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


async def get_unsent_posts_for_user(last_post_id: int | None):
    """Возвращает посты, которых пользователь ещё не видел."""
    async with async_session_maker() as session:
        query = select(Post).where(Post.id > (last_post_id or 0)).order_by(Post.id)
        result = await session.execute(query)
        return result.scalars().all()


async def update_user_last_post_id(user_id: int, post_id: int):
    """Обновляет last_post_id пользователя после отправки поста."""
    async with async_session_maker() as session:
        stmt = update(User).where(User.telegram_id == user_id).values(last_post_id=post_id)
        await session.execute(stmt)
        await session.commit()
