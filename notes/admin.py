from django.contrib import admin
from .models import Note
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('view_detail','user_nickname', 'book_title')

    def view_detail(self, obj):
        # ReadingRelation 객체의 변경 페이지 URL을 가져옵니다.
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}">Detail</a>', url)
    view_detail.short_description = 'View Detail'  # Admin 페이지의 컬럼 제목 설정

    def user_nickname(self, obj):
        # User 객체의 변경 페이지 URL을 가져옵니다.
        url = reverse('admin:%s_%s_change' % (obj.reading_relation.user._meta.app_label, obj.reading_relation.user._meta.model_name), args=[obj.reading_relation.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.reading_relation.user.nickname)
    user_nickname.short_description = 'User Nickname'  # Admin 페이지의 컬럼 제목 설정

    def book_title(self, obj):
        # Book 객체의 변경 페이지 URL을 가져옵니다.
        url = reverse('admin:%s_%s_change' % (obj.reading_relation.book._meta.app_label, obj.reading_relation.book._meta.model_name), args=[obj.reading_relation.book.pk])
        return format_html('<a href="{}">{}</a>', url, obj.reading_relation.book.title)
    book_title.short_description = 'Book Title'  # Admin 페이지의 컬럼 제목 설정