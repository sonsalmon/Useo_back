
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from books.models import Book, ReadingRelation
from notes.models import Note
from users.models import User


class NoteCreateSerializer(serializers.ModelSerializer):
    # nickname=serializers.SlugRelatedField(slug_field='nickname',queryset=User.objects.all())
    # isbn=serializers.SlugRelatedField(slug_field='isbn',queryset=Book.objects.all())
    book_isbn = serializers.CharField(write_only=True)

    class Meta:
        model = Note
        fields = ['book_isbn','content','add_date','last_modify']
    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data.pop('book_isbn')

        # ReadingRelation 객체를 user와 book으로 조회
        reading_relation = get_object_or_404(ReadingRelation, user=user, book=book)

        # Note 객체 생성
        note = Note.objects.create(reading_relation=reading_relation, **validated_data)
        return note

class NoteSerializer(serializers.ModelSerializer):
    book_isbn = serializers.CharField(write_only=True)

    class Meta:
        model = Note
        fields = ['book_isbn','reading_relation','content','add_date','last_modify',]
        extra_kwargs = {
            "reading_relation": {"read_only": True},
            "book_isbn":{"write_only":True},
            # 기타 필드 설정
        }
        # 여러 객체를 한번에 생성
    # def create(self,validated_data):
    #     print(validated_data)
    #     user = self.context['request'].user
    #     book = validated_data.pop('book_isbn')
    #     data_list = [validated_data]
    #     print(data_list)
    #
    #     # ReadingRelation 객체를 user와 book으로 조회
    #     reading_relation = get_object_or_404(ReadingRelation, user=user, book=book)
    #     # 멈춤
    #     # isbn값 받아서 적절한 reading relation을 찾아서 입력해야함
    #     # 근데 노트 리스트는 무조건 하나의 책에 대한 노트들임(책 읽으면서 작성하니까.)
    #     # validated_data.push('reading_relation',reading_relation)
    #     # print(**validated_data)
    #
    #     notes = [Note(reading_relation=reading_relation, **item) for item in data_list]
    #     return Note.objects.bulk_create(notes)

# 1개의 ReadingRelation이 N개의 Note를 가진다. 1:N 관계