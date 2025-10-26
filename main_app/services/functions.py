import asyncio

from main_app.core.bot_config import bot
from main_app.core.app_config import DELETE_AFTER_SECONDS
from main_app.core.logger import logger
from main_app.database.crud import search_all_posts, search_all_users, update_post_is_sent


async def send_posts(telegram_id):
    """ Функция отправки постов пользователям """

    # Получаем все неотправленные посты
    all_posts = await search_all_posts()
    if not all_posts:
        return

    posts = [post for post in all_posts if post.is_sent is False]

    sent_1 = None
    sent_2 = None

    for post in posts:
        try:
            if post.media_type == "photo":
                sent_1 = await bot.send_message(chat_id=telegram_id, text=post.message_text, protect_content=True)
                sent_2 = await bot.send_photo(chat_id=telegram_id, photo=post.media_file_id, protect_content=True)
            elif post.media_type == "video":
                sent_1 = await bot.send_message(chat_id=telegram_id, text=post.message_text, protect_content=True)
                sent_2 = await bot.send_video(chat_id=telegram_id, video=post.media_file_id, protect_content=True)
            elif post.media_type == "document":
                sent_1 = await bot.send_message(chat_id=telegram_id, text=post.message_text, protect_content=True)
                sent_2 = await bot.send_document(chat_id=telegram_id, document=post.media_file_id, protect_content=True)
            else:
                sent_1 = await bot.send_message(chat_id=telegram_id, text=post.message_text, protect_content=True)
        except Exception as ex:
            print(f"Ошибка при отправке пользователю {telegram_id} ПОСТа: {ex}")

        if DELETE_AFTER_SECONDS:
            asyncio.create_task(
                schedule_delete_message(
                    chat_id=telegram_id,
                    delay_seconds=DELETE_AFTER_SECONDS,
                    first_message_id=sent_1.message_id if sent_1 else None,
                    second_message_id=sent_2.message_id if sent_2 else None
                )
            )

        # Отмечаем пост как отправленный
        await update_post_is_sent(post.id)

        # Ждём 10 минут перед следующим постом
        await asyncio.sleep(5)


async def start_post_scheduler():
    """Постоянно работающий цикл рассылки"""
    while True:
        users = await search_all_users()
        for user in users:
            try:
                logger.info("Проверяем наличие новых постов...")
                await send_posts(user.telegram_id)
            except Exception as ex:
                logger.info(f"Ошибка в рассылке: {ex}")

        # Ожидание перед следующей проверкой БД
        await asyncio.sleep(10)  # каждые сутки 86400 проверять новые посты


async def schedule_delete_message(chat_id: int, delay_seconds: int, first_message_id=None, second_message_id=None):
    """Асинхронно подождать delay_seconds и удалить сообщение (если возможно)."""
    try:
        await asyncio.sleep(delay_seconds)
        if first_message_id:
            await bot.delete_message(chat_id=chat_id, message_id=first_message_id)
        if second_message_id:
            await bot.delete_message(chat_id=chat_id, message_id=second_message_id)
        logger.info("Удалено сообщение %s, %s в чате %s после %s сек.", first_message_id, second_message_id, chat_id, delay_seconds)
    except Exception as ex:
        logger.exception("Ошибка при попытке удалить сообщение %s, %s: %s", first_message_id, second_message_id, ex)
