
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from books.models import Book, ReadingRelation
from notes.models import Note
from users.models import User



class NoteListCreateSerializer(serializers.ModelSerializer):
    book_isbn = serializers.CharField(write_only=True)
    book_title = serializers.CharField(read_only=True,source='reading_relation.book.title')

    class Meta:
        model = Note
        fields = ['book_isbn','id','reading_relation','book_title','content','add_date','last_modify',]
        extra_kwargs = {
            "id":{"read_only":True},
            "reading_relation": {"read_only": True},
            "book_title": {"read_only": True},
            "book_isbn":{"write_only":True},
            # 기타 필드 설정
        }

# 1개의 ReadingRelation이 N개의 Note를 가진다. 1:N 관계

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields='__all__'
