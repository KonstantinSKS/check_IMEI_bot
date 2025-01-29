from django.db import models


class TgUser(models.Model):
    """Модель пользователя."""

    id = models.BigIntegerField(
        verbose_name='ID пользователя в Telegram',
        primary_key=True,
    )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=32,
        null=True,
        blank=True,
        default=None,
    )
    bot_unblocked = models.BooleanField(
        verbose_name='Бот разблокирован пользователем', default=True)
    is_unblocked = models.BooleanField(
        verbose_name='Пользователь разблокирован', default=True)
    token = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'#{self.id} {self.username}'
