from datetime import date, timedelta

from aiogram.types.user import User
from asgiref.sync import sync_to_async
from django.utils import timezone

from admin_panel.telegram.models import TgUser


@sync_to_async()
def tg_user_exists(tg_user_id: int) -> bool:
    """Проверка наличия пользователя в БД по tg_id."""

    return TgUser.objects.filter(id=tg_user_id).exists()


@sync_to_async
def create_tg_user(user: User, email: str, enter_full_name: str):
    """Создаёт и возвращает экземпляр пользователя TgUser."""

    tg_user = TgUser.objects.create(
        id=user.id,
        email=email,
        enter_full_name=enter_full_name,
        username=user.username,
        full_name=user.full_name
    )
    return tg_user
