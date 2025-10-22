import time

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable, Union


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, window: int = 10):
        """
        :param limit: сколько запросов можно сделать в пределах окна
        :param window: окно в секундах
        """
        self.limit = limit
        self.window = window
        self.users_calls: Dict[int, list[float]] = {}

    async def __call__(self, handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]], event: Union[Message, CallbackQuery], data: Dict[str, Any]) -> Any:
        user_id = (
            event.from_user.id
            if hasattr(event, "from_user") and event.from_user
            else None
        )
        if user_id is None:
            return await handler(event, data)

        now = time.time()
        calls = self.users_calls.setdefault(user_id, [])

        # очищаем старые записи
        self.users_calls[user_id] = [ts for ts in calls if now - ts <= self.window]

        if len(self.users_calls[user_id]) >= self.limit:
            # превысил лимит
            if isinstance(event, Message):
                await event.answer("⏳ Слишком часто! Попробуйте позже.")
            elif isinstance(event, CallbackQuery):
                await event.answer("⏳ Слишком часто! Попробуйте позже.", show_alert=True)
            return

        # добавляем текущий вызов
        self.users_calls[user_id].append(now)

        return await handler(event, data)
