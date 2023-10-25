
import requests

from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from requests import RequestException
from rest_framework import serializers
from books.models import Book, ReadingRelation

# remote url을 받아서 이미지 다운 후 ImageField에 저장하는 custom Field
class RemoteImageField(serializers.ImageField):
    def to_internal_value(self, data):
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
        fields = ['cover_image','isbn', 'title', 'author', 'description', 'publisher', 'publish_date',]

    def validate(self, data):
        # remote_image 필드의 값을 검증
        print('in validate :  ')
        print(data)
        cover_image = data.get('cover_image')
        if not cover_image:
            raise serializers.ValidationError({"cover_image": ["이미지 URL이 필요합니다."]})

        return data
class ReadingRelationCreateSerializer(serializers.ModelSerializer):
    '''
    두 가지 경우 존재
    1. 알라딘 open api로 책을 검색해서 서재에 추가 -> image 경로가 원격 url임
    2. 다른 유저의 서재에 있는 책을 내 서재에 추가 -> image 경로가 로컬 서버 경로임

    '''
    book_data = serializers.DictField(write_only=True)
    class Meta:
        model= ReadingRelation
        fields = ['book_data','reading_state','reading_duration', 'add_date','rate']
        # 다른 유저의 서재에서 책을 추가할 경우 아래 필드 없을 수 있음.
        extra_kwargs = {"reading_state": {"required": False, "allow_null": True, "default": 'READING'},
                        "reading_duration": {"required": False, "allow_null": True},
                        "rate": {"required": False, "allow_null": True},
                        }
    def create(self, validated_data):
        print(validated_data)
        user = self.context['request'].user # request에서 유저정보 가져옴
        book_data = validated_data.pop('book_data')

        # 이미지 다운
        cover_image_serializer = RemoteImageField()
        cover_image_path_or_url = book_data.get('cover_image')
        book_data['cover_image'] = cover_image_serializer.to_internal_value(cover_image_path_or_url)


        book, created = Book.objects.get_or_create(
            isbn=book_data.pop('isbn'),
            defaults=book_data
        )
        #생성된 게 아니라면 수정
        if not created:
            for key, value in book_data.items():
                setattr(book, key, value)
            book.save()
        reading_relation = ReadingRelation.objects.create(book=book, user=user, **validated_data)
        return reading_relation

# 독서 관계의 리스트
class ReadingRelationListSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(source='book.cover_image')
    nickname = serializers.CharField(source='user.nickname')
    class Meta:
        model = ReadingRelation
        fields =['cover_image', 'book', 'nickname']

class ReadingRelationRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    book_data = BookSerializer(read_only=True, source='book')

    class Meta:
        model = ReadingRelation
        fields= ['book_data', 'reading_state', 'add_date', 'rate']
        # exclude = ['user','book']
