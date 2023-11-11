from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from books.models import ReadingRelation
from notes.models import Note
from notes.serializers import NoteListCreateSerializer, NoteSerializer

'''
노트 생성, 리스트 생성, 특정 독서관계 노트 리스트 조회 -> NoteListCreateView
노트 상세 조회 
노트 수정
노트 삭제

'''
# class NoteUpdateDestroyView(generics.UpdateDestroyAPIView):
#     # get,put,patch,delete note
#     pass


# 노트 하나 / 리스트 생성, 노트 목록 조회
class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()

    serializer_class = NoteListCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 자신의 모든 노트 조회
        # 자신의 독서관계의 노트 조회
        # 다른 유저의 독서관계의 노트 조회
        nickname = self.request.query_params.get('nickname', None)
        isbn = self.request.query_params.get('isbn', None)
        print(nickname)
        queryset = Note.objects

        #특정 독서 관계에 대한 노트
        if (nickname is not None):

            queryset =queryset.filter(reading_relation__user__nickname=nickname)
            if isbn is None: #해당 유저의 모든 노트
                return queryset
            queryset = queryset.filter(reading_relation__book__isbn=isbn)
            return queryset


        # 현재 인증된 사용자의 메모만 조회
        return Note.objects.filter(reading_relation__user_id=self.request.user.pk)
    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        notes_data=serializer.validated_data
        user = self.request.user
        print(notes_data)
        if is_many:
            notes=[]
            for data in notes_data:
                book_isbn=data.pop('book_isbn')
                reading_relation=get_object_or_404(ReadingRelation,user=user,book__isbn=book_isbn)
                notes.append(Note(reading_relation=reading_relation,**data))
            Note.objects.bulk_create(notes)
        else:
            book_isbn=notes_data.pop('book_isbn')
            reading_relation=get_object_or_404(ReadingRelation,user=user,book__isbn=book_isbn)
            Note(reading_relation=reading_relation,**serializer.validated_data).save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)



class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

