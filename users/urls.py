from django.urls import path
from .views import RegisterView, LoginView, UserView, FollowingRelationView, FollowingRelationListView, \
    UserListByContainedKeyword

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('search/', UserListByContainedKeyword.as_view()),
    path('follow/',FollowingRelationView.as_view()),
    path('following_list/',FollowingRelationListView.as_view()),
]