"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views.user_view import UserViewSet
from users.views.hobby_view import HobbyViewSet
from users.views.invite_view import InviteViewSet
from users.views.birthday_view import BirthdayViewSet
from posts.views.event_view import EventViewSet

from django.conf import settings
from django.conf.urls.static import static

from users.views.user_hobby_view import UserHobbyViewSet

from users.views.type_hobby_view import TypeHobbyViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'hobbies', HobbyViewSet, basename='hobbies')
router.register(r'invites', InviteViewSet, basename='invites')
router.register(r'birthdays', BirthdayViewSet, basename='birthdays')
router.register(r'events', EventViewSet, basename='events')
router.register(r"user-hobbies", UserHobbyViewSet, basename="user-hobby")
router.register(r"type-hobbies", TypeHobbyViewSet, basename="type-hobbies")

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)