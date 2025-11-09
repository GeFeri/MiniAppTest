# backend/users/views/birthday_view.py

from rest_framework import viewsets, permissions, response
from rest_framework.response import Response
from users.services.user_service import UserService
from users.serializers import BirthdayUserSerializer

class BirthdayViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        users = UserService.list_birthdays(limit=30)
        serializer = BirthdayUserSerializer(users, many=True)
        return Response(serializer.data)