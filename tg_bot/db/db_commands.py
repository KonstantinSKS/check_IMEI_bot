from aiogram.types.user import User
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User as Model_User

from admin_panel.telegram.models import TgUser


@sync_to_async()
def create_super_user(username, password):
    """Автоматическое создание логина и пароля для суперпользователя."""

    if not Model_User.objects.filter(username=username).exists():
        Model_User.objects.create_superuser(username, password=password)


@sync_to_async
def get_tg_user(user_id):
    """Возвращает экземпляр требуемого пользователя по id."""

    return TgUser.objects.filter(id=user_id).first()


@sync_to_async()
def tg_user_exists(tg_user_id: int) -> bool:
    """Проверка наличия пользователя в БД по tg_id."""

    return TgUser.objects.filter(id=tg_user_id).exists()


@sync_to_async()
def update_user_token(tg_user_id: int, token: str):
    """Обновляет токен пользователя в БД."""

    return TgUser.objects.filter(id=tg_user_id).aupdate(token=token)


@sync_to_async
def create_tg_user(user: User, token: str):
    """Создаёт и возвращает экземпляр пользователя TgUser."""

    tg_user = TgUser.objects.create(
        id=user.id,
        username=user.username,
        token=token
    )
    return tg_user
