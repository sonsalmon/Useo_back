from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'nickname', 'profile_image', 'profile_message','library_latitude', 'library_longitude']
    pass

