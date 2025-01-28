from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import Message

from tg_bot.settings_logger import logger

# from tg_bot.config import logger
# from tg_bot.loader import bot
from tg_bot.states.all_states import StateUser
# from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards import reply as reply_kb
# from tg_bot.db import db_commands as db
from tg_bot.misc.utils import check_token, check_imei, validate_imei, get_service_list


base_reg_router = Router()


@base_reg_router.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    """Команда /start, отправка контакта."""
    logger.info(
        f"Пользователь {message.from_user.full_name} ввел(a) команду /start"
    )
    await message.answer(
        text=f"Здравствуйте, {message.from_user.first_name}. "
        "Для авторизации введите ваш токен API Sandbox или токен API Live.",
        # reply_markup=reply_kb.send_contact(),
    )
    await state.set_state(StateUser.enter_token)


@base_reg_router.message(StateUser.enter_token)
async def get_token(message: Message, state: FSMContext):
    """Авторизация и проверка токена."""

    try:
        token_data = await check_token(message.text)

        if token_data["status"] == "unauthorized":
            await message.answer(
                "Неверный токен. Пожалуйста, проверьте и введите правильный токен."
            )
            return

        service_list = await get_service_list(message.text)

        if not service_list:
            await message.answer(
                "Указанный токен не предоставляет доступных бесплатных сервисов. "
                "Пожалуйста, введите другой токен."
            )
            await state.set_state(StateUser.enter_token)
            return

        await state.update_data(token=message.text)
        await message.answer(
            "Токен успешно подтверждён. Теперь введите IMEI устройства:"
        )
        await state.set_state(StateUser.get_imei)

    except Exception as e:
        await message.answer(
            "Произошла ошибка при проверке токена. Попробуйте выполнить запрос позже."
        )
        logger.error(f"Ошибка при проверке токена: {e}")


@base_reg_router.message(StateUser.get_imei)
async def process_imei(message: Message, state: FSMContext):
    """Получение IMEI, вызов функции check_imei и возврат информации пользователю."""
    imei = message.text

    if not validate_imei(imei):
        await message.answer(
            "Некорректный IMEI. Убедитесь, что вы ввели 15 цифр.")
        return

    user_data = await state.get_data()
    token = user_data.get("token")

    try:
        imei_info = await check_imei(imei, token)

        if isinstance(imei_info, str):
            await message.answer(
                "Указанный IMEI не найден в imeicheck.net. "
                "Проверьте значение или попробуйте другое устройство.")
        else:
            await message.answer(
                f"Информация о IMEI:\n\n{imei_info}"
            )

    except Exception as e:
        await message.answer("Произошла ошибка при обработке IMEI. Попробуйте позже.")
        logger.error(f"Ошибка при обработке IMEI: {e}")


@base_reg_router.message(Command("help"))
async def command_help(message: types.Message):
    """Обработка команды /help."""
    await message.answer("Для запуска или перезапуска бота напишите /start")
