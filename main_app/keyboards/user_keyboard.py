from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class USER_KB:
    @staticmethod
    def privacy_kb():
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="ДА, СОГЛАСЕН(А)", callback_data="conf_privacy")
            ]]
        )

    @staticmethod
    def watching_video(id_video: int):
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="СМОТРЕТЬ ВИДЕО", callback_data=f"watching_video_{id_video}")
            ]]
        )

