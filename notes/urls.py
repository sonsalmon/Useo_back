from django.urls import path
from .views import NoteCreateView, NoteListCreateView, NoteListRetrieveView, NoteListByUserView

urlpatterns = [
    path('create/', NoteCreateView.as_view(), name='note-create'),
    path('create/list/', NoteListCreateView.as_view(), name='note-list-create'),
    path('get_list/',NoteListCreateView.as_view()),
]