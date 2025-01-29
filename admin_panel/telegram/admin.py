from django.contrib import admin
from django.contrib.auth.models import Group

from admin_panel.telegram.models import TgUser


admin.site.unregister(Group)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'is_unblocked',
        'bot_unblocked',
    )

    def has_add_permission(self, request, obj=None):
        """Убирает возможность создания пользователей через админку."""
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                'id', 'username', 'bot_unblocked', 'token')
        return self.readonly_fields
