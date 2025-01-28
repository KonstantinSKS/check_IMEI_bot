from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def send_contact():
    """Клавиатура для отправки номера телефона"""
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Отправить контакт", request_contact=True)
    return keyboard.adjust(1).as_markup(resize_keyboard=True)
