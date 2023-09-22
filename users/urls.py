from django.urls import include, path

from users.views import hello_world

urlpatterns = [
    path('hello_world/', hello_world)
]
