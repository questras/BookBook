from django.contrib import admin

from .models import AuthToken


class AuthTokenManager(admin.ModelAdmin):
    """AuthToken manager which mainly hides useless options and allows searching by tokens user email."""

    exclude = ('token', 'expiry')
    list_display = ('user', 'device', 'created', 'expires', 'token')
    list_filter = ('user__email', 'created', 'expires')
    list_editable = ('expires', 'device')

    search_fields = ['user__email']

    ordering = ('user__email', 'expires')

    def save_model(self, request, obj, form, change):
        return AuthToken.objects.create(obj.user, obj.device)


admin.site.register(AuthToken, AuthTokenManager)
