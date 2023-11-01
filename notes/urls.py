from django.urls import path
from .views import NoteListCreateView, NoteRetrieveUpdateDestroyView

urlpatterns = [
    path('list/', NoteListCreateView.as_view(), name='note-list-create-or-get'),
    path('note/<int:pk>/', NoteRetrieveUpdateDestroyView.as_view()),
    # path('patch/<int:pk>',NoteRetrieveUpdateDestroyView.as_view()),
    # path('delete/<int:pk>',NoteRetrieveUpdateDestroyView.as_view()),
]