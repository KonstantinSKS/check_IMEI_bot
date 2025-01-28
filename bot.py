import asyncio
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import BotCommand

from tg_bot.loader import dp, bot
# from .config import super_user_name, super_user_pass, logger
# from .middlewares import
from tg_bot.settings_logger import logger
# from .misc import start_milling
# from .db.db_commands import create_super_user


async def set_commands():
    """Функция для формирования списка команд для кнопки Menu."""

    commands = [BotCommand(command="/start", description="Запустить бота")]
    await bot.set_my_commands(commands=commands)


async def main():
    """Функция запуска бота."""

    logger.info('Запуск бота')

    await set_commands()

    # dp.message.outer_middleware(UserMiddleware())
    # dp.callback_query.outer_middleware(UserMiddleware())

    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(
    #     start_milling,
    #     'interval',
    #     minutes=1,
    #     kwargs={'bot': bot}
    # )
    # scheduler.start()  # Запуск планировщика

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
