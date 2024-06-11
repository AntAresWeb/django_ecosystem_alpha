from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email',)
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)
