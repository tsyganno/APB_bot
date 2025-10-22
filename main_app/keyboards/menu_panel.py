from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


USER_COMMANDS = [
    BotCommand(command="start", description="Начать сначала"),
]

ADMIN_COMMANDS = [
    BotCommand(command="start", description="Начать сначала"),
]


async def set_user_commands(bot: Bot, user_id: int):
    """Устанавливает команды для пользователя"""
    await bot.set_my_commands(
        commands=USER_COMMANDS,
        scope=BotCommandScopeChat(chat_id=user_id)
    )


async def set_admin_commands(bot: Bot, user_id: int):
    """Устанавливает команды для поставщика"""
    await bot.set_my_commands(
        commands=ADMIN_COMMANDS,
        scope=BotCommandScopeChat(chat_id=user_id)
    )


async def clear_commands(bot: Bot, user_id: int):
    """Удаляет команды у пользователя"""
    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=user_id))