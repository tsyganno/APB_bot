from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    admin = State()


class PostState(StatesGroup):
    text = State()
    media = State()
    confirm = State()
