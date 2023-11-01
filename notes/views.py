from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from books.models import ReadingRelation
from notes.models import Note
from notes.serializers import NoteSerializer, NoteCreateSerializer



'''
노트 생성
노트 수정
노트 삭제
노트 조회
노트 리스트 생성
노트 리스트 조회(독서관계의)
특정 유저의 노트 리스트 조회

'''




class NoteCreateView(generics.CreateAPIView):
    serializer_class = NoteCreateSerializer


    #create note
    pass
# class NoteUpdateDestroyView(generics.UpdateDestroyAPIView):
#     # get,put,patch,delete note
#     pass
class NoteRetrieveView(generics.RetrieveAPIView):
    pass


class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()

    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 자신의 모든 노트 조회
        # 자신의 독서관계의 노트 조회
        # 다른 유저의 독서관계의 노트 조회
        nickname = self.request.query_params.get('nickname', None)
        isbn = self.request.query_params.get('isbn', None)
        print(nickname)
        queryset = Note.objects

        if (nickname is not None) & (isbn is not None):
            print(isbn)

            queryset =queryset.filter(reading_relation__user__nickname=nickname)
            queryset = queryset.filter(reading_relation__book__isbn=isbn)
            return queryset

        # 현재 인증된 사용자의 메모만 조회
        return Note.objects.filter(reading_relation__user_id=self.request.user.pk)
    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        if is_many:
            notes_data=serializer.validated_data
            user = self.request.user
            notes=[]
            for data in notes_data:
                book_isbn=data.pop('book_isbn')
                reading_relation=get_object_or_404(ReadingRelation,user=user,book__isbn=book_isbn)
                notes.append(Note(reading_relation=reading_relation,**data))
            Note.objects.bulk_create(notes)
        else:
            self.perform_create(serializer)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class NoteListRetrieveView(generics.ListAPIView):

    # 리스트 조회
    pass
class NoteListByUserView(generics.ListAPIView):
    # 특정 유저 리스트 조회
    pass
