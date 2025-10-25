import asyncio


from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher


from main_app.handlers.user import start
from main_app.handlers.admin import admin, posts
from main_app.core.bot_config import bot
from main_app.core.logger import logger
from main_app.services.middleware import ThrottlingMiddleware


async def main():
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.message.middleware(ThrottlingMiddleware(limit=1, window=1))
    dp.callback_query.middleware(ThrottlingMiddleware(limit=1, window=1))

    # Подключаем роутеры (admin)
    dp.include_router(admin.admin_router)
    dp.include_router(posts.post_router)

    # Подключаем роутеры (user)
    dp.include_router(start.start_router)

    logger.info("Бот успешно запущен")
    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен вручную")
    finally:
        logger.info("Останавливаем polling...")
        await dp.storage.close()
        await bot.session.close()
        logger.info("Ресурсы бота освобождены")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен вручную.")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

