from django.urls import path
from .views import ReadingRelationCreateView, ReadingRelationListView, ReadingRelationRetrieveUpdateDestroyView

urlpatterns = [
    path('create/', ReadingRelationCreateView.as_view()),
    path('get_list/', ReadingRelationListView.as_view(), name='get_list'),
    path('get_update_destroy/<str:nickname>/<str:isbn>/', ReadingRelationRetrieveUpdateDestroyView.as_view()),
    # path('get/<str:nickname>/<str:isbn>/', ReadingRelationRetrieveView.as_view()),
]