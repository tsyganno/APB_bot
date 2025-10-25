from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from asyncio import sleep

from main_app.states.states import UserState, PostState
from main_app.keyboards.admin_keyboard import ADMIN_KB
from main_app.services.middleware import IsAdmin
from main_app.database.crud import search_all_users

admin_router = Router()
admin_router.message.filter(IsAdmin())


@admin_router.message(IsAdmin(), F.text == "/admin_panel")
async def admin_panel(message: Message, state: FSMContext):
    await message.answer("Выбери действие.", reply_markup=ADMIN_KB.admin_kb())
    await state.set_state(UserState.admin)


@admin_router.message(UserState.admin, IsAdmin())
async def handle_admin_panel_selection(message: Message, state: FSMContext):
    text = message.text.strip()

    if text == "👫 Количество пользователей":
        all_users = await search_all_users()
        if all_users:
            await message.answer(f"В БД: {len(all_users)} пользователей.")
        else:
            await message.answer(f"В БД: 0 пользователей.")

    elif text == "📢 Загрузить пост в БД":
        await state.set_state(PostState.text)
        await message.answer("Введите текст поста (описание к медиа тоже сюда):")

    elif text == "📧 Excel-отчеты на email":
        pass

    elif text == "🔙 Назад":
        await state.clear()
        await message.answer("Вы вышли из панели администратора.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Неизвестная команда. Пожалуйста, выберите одну из кнопок.")
