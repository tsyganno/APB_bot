from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest


from main_app.core.bot_config import bot
from main_app.core.app_config import settings
from main_app.core.logger import logger
from main_app.keyboards.menu_panel import set_admin_commands, set_user_commands, clear_commands
from main_app.services.functions import send_posts
from main_app.keyboards.user_keyboard import USER_KB
from main_app.database.crud import save_user_to_db

start_router = Router()


@start_router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id in settings.list_admin_id:  # id админа в config.py
        await set_admin_commands(bot, message.from_user.id)
        await message.answer("👋 Привет, Админ!\n\nНажми кнопку 'МЕНЮ' для выбора действий.")
    else:
        await clear_commands(bot, message.from_user.id)
        await message.answer("Чтобы получить «20 шагов для запуска импорта», нужно ваше согласие ниже ⬇️👇\n\n"
            "Вы соглашаетесь:\n"
            "1. На обработку персональных данных в соответствии (ссылка) с Политикой конфиденциальности (ссылка)\n"
            "2. На получение информационных материалов и рассылок (ссылка)\n\n"
            "Письма будут по делу.\n"
            "От практикующего предпринимателя, импортера, консультанта по систематизации бизнеса, тренера по продажам да и просто активного человека, любящего свою жизнь🔥\n\n"
            "Вы даёте своё согласие?\n\n"
            "Да, соглашаюсь\n"
            "(Давайте уже связки, я выгорел/а)⤵", reply_markup=USER_KB.privacy_kb())


@start_router.callback_query(F.data.startswith("conf_privacy"))
async def conf_privacy(callback: CallbackQuery, state: FSMContext):
    await state.update_data(name=f"{callback.from_user.last_name} {callback.from_user.first_name}")
    user_data = await state.get_data()
    try:
        await save_user_to_db(user_data, callback.from_user.id, callback.from_user.username)
    except Exception as ex:
        logger.error(f"Неизвестная ошибка при записи пользователя в БД: {ex}")
    # await callback.message.answer("Поздравляю! Ты запустил бота и теперь можешь бесплатно забрать гайд!"
    #                               "\n\nЖелаю приятного просмотра!"
    #                               "\n\nВидео ниже.", reply_markup=USER_KB.watching_video(1))

    await send_posts()

