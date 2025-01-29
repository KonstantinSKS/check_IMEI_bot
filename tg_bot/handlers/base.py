from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import Message

from tg_bot.db import db_commands as db
from tg_bot.settings_logger import logger
from tg_bot.states.all_states import StateUser
from tg_bot.keyboards import reply as reply_kb
from tg_bot.misc.utils import (check_token, check_imei, validate_imei,
                               get_service_list)
from tg_bot.misc.constants import HELP_TEXT


base_reg_router = Router()


@base_reg_router.message(Command("help"))
async def command_help(message: types.Message):
    """Обработка команды /help."""

    await message.answer(HELP_TEXT)


@base_reg_router.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    """Команда /start, отправка контакта."""
    logger.info(
        f"Пользователь {message.from_user.full_name} ввел(a) команду /start"
    )
    if await db.tg_user_exists(message.from_user.id):
        await message.answer(
            "Введите IMEI устройства:",
            reply_markup=reply_kb.imei_keyboard()
        )
        await state.set_state(StateUser.get_imei)

    else:
        await message.answer(
            text=f"Здравствуйте, {message.from_user.first_name}. "
            "Для авторизации введите ваш токен API Sandbox или токен API Live."
        )
        await state.set_state(StateUser.enter_token)


@base_reg_router.message(StateUser.enter_token)
async def get_token(message: Message, state: FSMContext):
    """Авторизация и проверка токена."""

    try:
        token_data = await check_token(message.text)

        if token_data["status"] == "unauthorized":
            await message.answer(
                "Неверный токен. "
                "Пожалуйста, проверьте и введите правильный токен."
            )
            return

        service_list = await get_service_list(message.text)

        if not service_list:
            await message.answer(
                "Указанный токен не предоставляет "
                "доступных бесплатных сервисов. "
                "Пожалуйста, введите другой токен."
            )
            await state.set_state(StateUser.enter_token)
            return

        if not await db.tg_user_exists(message.from_user.id):
            await db.create_tg_user(
                user=message.from_user,
                token=message.text
            )
        else:
            await db.update_user_token(message.from_user.id, message.text)

        await message.answer("Вы успешно авторизованы.")
        await message.answer("Введите IMEI устройства.")

        await state.set_state(StateUser.get_imei)

    except Exception as e:
        await message.answer(
            "Произошла ошибка при проверке токена. "
            "Попробуйте выполнить запрос позже."
        )
        logger.error(f"Ошибка при проверке токена: {e}")


@base_reg_router.message(F.text == "Отправить IMEI")
async def ask_for_imei(message: Message, state: FSMContext):
    """Обработка нажатия на кнопку 'Отправить IMEI'."""

    await message.answer("Введите IMEI устройства:")
    await state.set_state(StateUser.get_imei)


@base_reg_router.message(StateUser.get_imei)
async def process_imei(message: Message, state: FSMContext):
    """Получение IMEI, вызов функции check_imei
    и возврат информации пользователю."""

    imei = message.text
    user = await db.get_tg_user(message.from_user.id)

    if not user:
        await message.answer(
            "Ваш аккаунт был удален. "
            "Пожалуйста, обратитесь к администратору "
            "или зарегистрируйтесь заново.")
        return

    if not validate_imei(imei):
        await message.answer(
            "Некорректный IMEI. Убедитесь, что вы ввели 15 цифр.")
        return

    try:
        imei_info = await check_imei(imei, user.token)

        if isinstance(imei_info, str):
            await message.answer(
                "Указанный IMEI не найден в imeicheck.net. "
                "Проверьте значение или попробуйте другое устройство.")
        else:
            await message.answer(
                f"Информация о IMEI:\n\n{imei_info}"
            )

    except Exception as e:
        await message.answer(
            "Произошла ошибка при обработке IMEI. Попробуйте позже.")
        logger.error(f"Ошибка при обработке IMEI: {e}")
