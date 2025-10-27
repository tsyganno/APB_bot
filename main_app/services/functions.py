import asyncio

from main_app.core.bot_config import bot
from main_app.core.app_config import DELETE_AFTER_SECONDS
from main_app.core.logger import logger
from main_app.database.crud import search_all_users, get_unsent_posts_for_user, update_user_last_post_id


async def send_single_post(telegram_id, post):
    sent_1 = sent_2 = None
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

        # Удаляем после времени, если нужно
        if DELETE_AFTER_SECONDS:
            asyncio.create_task(
                schedule_delete_message(
                    chat_id=telegram_id,
                    delay_seconds=DELETE_AFTER_SECONDS,
                    first_message_id=sent_1.message_id if sent_1 else None,
                    second_message_id=sent_2.message_id if sent_2 else None
                )
            )
    except Exception as ex:
        logger.error(f"Ошибка при отправке пользователю {telegram_id}: {ex}")


async def start_post_scheduler():
    """Постоянно работающий цикл рассылки."""
    while True:
        users = await search_all_users()
        if not users:
            await asyncio.sleep(10)
            continue

        for user in users:
            # Получаем все посты, которых этот пользователь ещё не видел
            unsent_posts = await get_unsent_posts_for_user(user.last_post_id)
            if not unsent_posts:
                continue

            for post in unsent_posts:
                try:
                    await send_single_post(user.telegram_id, post)
                    await update_user_last_post_id(user.telegram_id, post.id)
                    await asyncio.sleep(10)  # пауза между постами (10 сек)
                except Exception as ex:
                    logger.error(f"Ошибка при отправке поста {post.id} пользователю {user.telegram_id}: {ex}")

        await asyncio.sleep(10)


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
