from django.urls import path
from .views import NoteListCreateView, NoteRetrieveUpdateDestroyView

urlpatterns = [
    path('create/list/', NoteListCreateView.as_view(), name='note-list-create'),
    path('get_list/',NoteListCreateView.as_view()),
    path('note/<int:pk>/', NoteRetrieveUpdateDestroyView.as_view()),
    # path('patch/<int:pk>',NoteRetrieveUpdateDestroyView.as_view()),
    # path('delete/<int:pk>',NoteRetrieveUpdateDestroyView.as_view()),
]