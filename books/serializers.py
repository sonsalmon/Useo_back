
import requests

from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from requests import RequestException
from rest_framework import serializers
from books.models import Book, ReadingRelation
from notes.serializers import NoteSerializer


# remote url을 받아서 이미지 다운 후 ImageField에 저장하는 custom Field
class RemoteImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # 문제점 : 이미 이미지가 있어도 다운?
        print('downloading remote url image...')
        if isinstance(data, str) and data.startswith(('http://', 'https://')):
            try:
                response = requests.get(data)
                response.raise_for_status()  # HTTP 에러 발생 시 예외를 발생시킵니다.
                image_name = data.split('/')[-1].split('?')[0]
                data = ContentFile(response.content, name=image_name)
            except requests.RequestException:
                raise serializers.ValidationError("이미지 다운로드에 실패했습니다.")
        return super().to_internal_value(data)

class BookSerializer(serializers.ModelSerializer):
    #model field와 연결
    cover_image = RemoteImageField(required=True)#, source='cover_image')
    class Meta:
        model= Book
        fields = ['isbn', 'title', 'author', 'description', 'publisher', 'publish_date','cover_image',]

    def validate_isbn(self, isbn):
        # ISBN이 이미 존재하는지 확인
        book = Book.objects.filter(isbn=isbn).first()
        if book:
            return book
        return isbn

class ReadingRelationCreateSerializer(serializers.ModelSerializer):
    '''
    두 가지 경우 존재
    1. 알라딘 open api로 책을 검색해서 서재에 추가 -> image 경로가 원격 url임
    2. 다른 유저의 서재에 있는 책을 내 서재에 추가 -> image 경로가 로컬 서버 경로임

    '''
    book_data = serializers.DictField(write_only=True)
    # book_data = BookSerializer(source='book')
    class Meta:
        model= ReadingRelation
        fields = ['book_data','reading_state','reading_progress','reading_duration', 'add_date','rate']
        # 다른 유저의 서재에서 책을 추가할 경우 아래 필드 없을 수 있음.
        extra_kwargs = {"reading_state": {"required": False, "allow_null": True, "default": 'READING'},
                        "reading_duration": {"required": False, "allow_null": True},
                        "rate": {"required": False, "allow_null": True},
                        "reading_progress":{"required": False},
                        }
    def create(self, validated_data):
        print(validated_data)
        user = self.context['request'].user # request에서 유저정보 가져옴
        book_data = validated_data.pop('book_data')

        book, book_created = Book.objects.get_or_create(
            isbn=book_data.pop('isbn'),
        )
        # 책이 새로 생성되었다면 이미지 다운 및 정보 입력
        if book_created:
            # 이미지 다운
            cover_image_serializer = RemoteImageField()
            cover_image_path_or_url = book_data.get('cover_image')
            book_data['cover_image'] = cover_image_serializer.to_internal_value(cover_image_path_or_url)
            for key, value in book_data.items():
                setattr(book, key, value)
            book.save()

        reading_relation, created= ReadingRelation.objects.get_or_create(book=book, user=user, **validated_data)
        # 관계가 이미 존재하면 해당 관계를 수정
        if not created:
            for key, value in validated_data.items():
                setattr(reading_relation, key, value)
            reading_relation.save()
        return reading_relation

# 독서 관계의 리스트
class ReadingRelationListSerializer(serializers.ModelSerializer):
    # cover_image = serializers.ImageField(source='book.cover_image')
    nickname = serializers.CharField(source='user.nickname')
    # author = serializers.CharField(source='book.author')
    book_data = BookSerializer(source='book')
    class Meta:
        model = ReadingRelation
        # fields =['cover_image', 'book', 'nickname', 'author', 'reading_state']
        fields =['book_data','nickname', 'reading_state', 'reading_duration','reading_progress','add_date', 'rate']

class ReadingRelationRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    book_data = BookSerializer(read_only=True, source='book')

    class Meta:
        model = ReadingRelation
        fields= ['book_data', 'reading_state', 'reading_progress','reading_duration', 'rate', 'add_date']
        extra_kwargs ={"add_date":{"read_only" : True},
                       "book_data":{"read_only": True}
                       }
        # exclude = ['user','book']




class ReadingRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReadingRelation
        fields='__all__'

