from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, FollowingRelation


# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'nickname', 'profile_image', 'profile_message','library_latitude', 'library_longitude']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': ('nickname', 'profile_image', 'profile_message', 'library_latitude', 'library_longitude')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional info', {'fields': ('nickname', 'profile_image', 'profile_message', 'library_latitude', 'library_longitude')}),
    )

@admin.register(FollowingRelation)
class FollowingRelationAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following']
    
