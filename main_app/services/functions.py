import asyncio

from main_app.core.bot_config import bot
from main_app.core.logger import logger
from main_app.database.crud import search_all_posts, search_all_users, update_post_is_sent


async def send_posts():
    """ Функция отправки постов пользователям """

    # Получаем все неотправленные посты
    posts = [post for post in await search_all_posts() if post.is_sent is False]

    if not posts:
        return

    # Получаем список пользователей
    users = await search_all_users()

    for post in posts:
        for user in users:
            try:
                if post.media_type == "photo":
                    await bot.send_photo(chat_id=user.telegram_id, video=post.media_file_id, caption=post.message_text)
                elif post.media_type == "video":
                    await bot.send_video(chat_id=user.telegram_id, video=post.media_file_id, caption=post.message_text)
                elif post.media_type == "document":
                    await bot.send_document(chat_id=user.telegram_id, document=post.media_file_id, caption=post.message_text)
                else:
                    await bot.send_message(chat_id=user.telegram_id, text=post.message_text)
            except Exception as ex:
                print(f"Ошибка при отправке пользователю {user.telegram_id} ПОСТа: {ex}")

        # Отмечаем пост как отправленный
            await update_post_is_sent(post.id)

            # Ждём 10 минут перед следующим постом
            await asyncio.sleep(5)


async def start_post_scheduler():
    """Постоянно работающий цикл рассылки"""
    while True:
        try:
            logger.info("Проверяем наличие новых постов...")
            await send_posts()
        except Exception as ex:
            logger.info(f"❌ Ошибка в рассылке: {ex}")

        # Ожидание перед следующей проверкой БД
        await asyncio.sleep(5)  # каждые сутки 86400 проверять новые посты

