from django.contrib import admin
from .models import Book, ReadingRelation
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'title')

    def isbn(self, obj):
        return obj.book.isbn
    isbn.short_description = 'book isbn'

    def title(self, obj):
        return obj.book.title
    title.short_description = 'book title'



@admin.register(ReadingRelation)
class ReadingRelationAdmin(admin.ModelAdmin):
    list_display = ('view_detail','user_nickname', 'book_title')

    def user_nickname(self, obj):
        # User 객체의 변경 페이지 URL을 가져옵니다.
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name), args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.nickname)
    user_nickname.short_description = 'User Nickname'  # Admin 페이지의 컬럼 제목 설정

    def book_title(self, obj):
        # Book 객체의 변경 페이지 URL을 가져옵니다.
        url = reverse('admin:%s_%s_change' % (obj.book._meta.app_label, obj.book._meta.model_name), args=[obj.book.pk])
        return format_html('<a href="{}">{}</a>', url, obj.book.title)
    book_title.short_description = 'Book Title'  # Admin 페이지의 컬럼 제목 설정

    def view_detail(self, obj):
        # ReadingRelation 객체의 변경 페이지 URL을 가져옵니다.
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}">Detail</a>', url)
    view_detail.short_description = 'View Detail'  # Admin 페이지의 컬럼 제목 설정


