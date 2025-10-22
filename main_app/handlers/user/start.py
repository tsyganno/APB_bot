from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest


from main_app.core.bot_config import bot
from main_app.core.app_config import settings
from main_app.keyboards.menu_panel import set_admin_commands, set_user_commands, clear_commands
from main_app.keyboards.admin_keyboard import ADMIN_KB
from main_app.keyboards.user_keyboard import USER_KB

start_router = Router()


@start_router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == settings.admin_id:  # id админа в config.py
        await set_admin_commands(bot, message.from_user.id)
        await message.answer(
            "👋 Привет, Админ!\n\nЧто хочешь сделать?",
            reply_markup=ADMIN_KB.admin_start_kb()
        )
    else:
        await clear_commands(bot, message.from_user.id)
        await message.answer("Чтобы получить «5 лучших связок для рекордного запуска/месяца по прибыли», нужно ваше согласие ниже👇\n\n"
            "Вы соглашаетесь:\n"
            "1. На обработку персональных данных в соответствии (https://wowdengi.com/pers_dan) с Политикой конфиденциальности (https://wowdengi.com/pol_pers_dan)\n"
            "2. На получение информационных материалов и рассылок (https://wowdengi.com/pol_rassilok)\n\n"
            "Письма будут по делу.\n"
            "От продюсера очень крупных школ и ex-руководителя по маркетингу компании из топ-11 EdTech России по обороту.\n"
            "С инструментами.\n"
            "C заботой.\n"
            "😇❤\n\n"
            "Вы даёте своё согласие?\n\n"
            "Да, соглашаюсь\n"
            "(Давайте уже связки, я выгорел/а)⤵", reply_markup=USER_KB.privacy_kb())
