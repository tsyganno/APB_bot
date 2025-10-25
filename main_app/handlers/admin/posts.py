from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from main_app.core.app_config import created_at_irkutsk_tz
from main_app.states.states import PostState, UserState
from main_app.core.logger import logger
from main_app.database.models import Post
from main_app.services.middleware import IsAdmin
from main_app.database.session import async_session_maker

post_router = Router()
post_router.message.filter(IsAdmin())


@post_router.message(PostState.text, IsAdmin())
async def set_broadcast_text(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(message_text=message.text)
        await message.answer("Пришлите медиафайл (фото/видео/документ) или напишите 'нет':")
        await state.set_state(PostState.media)
    else:
        await message.answer("Введите текст ПОСТа 'текстом'.")


@post_router.message(PostState.media, IsAdmin())
async def set_broadcast_media(message: Message, state: FSMContext):
    media_file_id = None
    media_type = None

    if message.photo:
        media_file_id = message.photo[-1].file_id
        media_type = "photo"
    elif message.video:
        media_file_id = message.video.file_id
        media_type = "video"
    elif message.document:
        media_file_id = message.document.file_id
        media_type = "document"

    await state.update_data(media_file_id=media_file_id, media_type=media_type)
    data = await state.get_data()
    preview = f"📢 <b>Предпросмотр рассылки</b>\n\n{data['message_text']}\n"
    await message.answer(preview, parse_mode="HTML")
    await message.answer("Сохранить? (да/нет)")
    await state.set_state(PostState.confirm)


@post_router.message(PostState.confirm, IsAdmin())
async def confirm_broadcast(message: Message, state: FSMContext):
    if message.text.lower() != "да":
        await message.answer("Рассылка отменена.")
        return await state.clear()

    data = await state.get_data()
    try:
        async with async_session_maker() as session:
            post = Post(
                message_text=data["message_text"],
                media_file_id=data.get("media_file_id"),
                media_type=data.get("media_type"),
                created_at=created_at_irkutsk_tz
            )
            session.add(post)
            await session.commit()
            await message.answer(f"ПОСТ успешно сохранен в БД ✅.")
    except Exception as ex:
        logger.error(f"Неизвестная ошибка при сохранения ПОСТа в БД: {ex}")
        await message.answer(f"Ошибка при сохранении ПОСТа в БД ❌.")

    await state.set_state(UserState.admin)
