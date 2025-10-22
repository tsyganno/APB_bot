from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class USER_KB:
    @staticmethod
    def privacy_kb():
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да, согласен(а)", callback_data="conf_privacy")]])
