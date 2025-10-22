from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ADMIN_KB:
    @staticmethod
    def admin_start_kb() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📝 Зарегистрироваться как пользователь")],
                [KeyboardButton(text="🛠 Панель администратора")],
                [KeyboardButton(text="🙈 Пока ничего не делать")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
