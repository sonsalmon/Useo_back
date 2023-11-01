from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import generics, permissions, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import UpdateModelMixin

from books.models import ReadingRelation, Book
from books.serializers import BookSerializer, ReadingRelationCreateSerializer, ReadingRelationListSerializer, \
   ReadingRelationRetrieveUpdateDestroySerializer, ReadingRelationWithNoteSerializer
from users.models import User

'''
본인 유저의 독서관계 생성 (이때 필요하다면 도서 생성)
특정 유저의 독서관계 리스트 조회
본인의 독서관계 수정
본인의 독서관계 삭제 (아무 독서관계도 책을 참조하지 않으면 도서도 삭제)

도서 정보 조회
'''

# Create your views here.
class BookCreatApiView(generics.CreateAPIView):
   serializer_class = BookSerializer

class ReadingRelationCreateView(generics.CreateAPIView):
   serializer_class = ReadingRelationCreateSerializer

# 독서관계 리스트 조회
class ReadingRelationListView(generics.ListAPIView):
   serializer_class = ReadingRelationListSerializer
   def get_queryset(self):
      nickname = self.request.query_params.get('nickname', None)

      # username이 주어지지 않았거나 요청을 보낸 사용자와 일치하는 경우
      if not nickname or nickname == self.request.user.username:
         print('not username or username ==request.username')
         return ReadingRelation.objects.filter(user=self.request.user)
      #
      # nickname으로 다른 사용자의 정보를 조회하려는 경우 (예: 관리자 등)
      return ReadingRelation.objects.filter(user__nickname=nickname)


#독서관계 조회/수정/삭제
# 삭제시 204 No Content 응답
class ReadingRelationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   serializer_class = ReadingRelationRetrieveUpdateDestroySerializer
   def get_object(self):
      # URL에서 username과 book_isbn 값을 가져옵니다.
      user_nickname = self.kwargs['nickname']
      book_isbn = self.kwargs['isbn']

      # User와 Book 모델을 사용하여 해당 객체를 가져옵니다.
      user = get_object_or_404(User, nickname=user_nickname)
      book = get_object_or_404(Book, isbn=book_isbn)
      print(user)
      print(book)

      # ReadingRelation 객체를 user와 book을 사용하여 조회합니다.
      obj = get_object_or_404(ReadingRelation, user=user, book=book)
      return obj


