from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ADMIN_KB:
    @staticmethod
    def admin_kb() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👫 Количество пользователей")],
                [KeyboardButton(text="📢 Загрузить пост в БД")],
                [KeyboardButton(text="📧 Excel-отчеты на email")],
                [KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
