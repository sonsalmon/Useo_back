"""
URL configuration for Useo_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include



# url로 서버 상의 MEDIA_ROOT 접근 제한
def protected_file(request, path, document_root=None):
    from django.contrib import messages
    messages.error(request, "접근 불가")
    return redirect('/')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('notes/', include('notes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
