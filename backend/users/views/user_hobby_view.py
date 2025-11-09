# backend/users/views/user_hobby_view.py
from rest_framework import viewsets, permissions, response, status
from users.services.user_hobby_service import UserHobbyService
from users.serializers import UserHobbySerializer

class UserHobbyViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.AllowAny]  # пока без auth

    def list(self, request):
        user = request.user
        hobbies = UserHobbyService.list_user_hobbies(user)
        return response.Response(UserHobbySerializer(hobbies, many=True).data)

    def create(self, request):
        hobby_id = request.data.get("hobby_id")
        description = request.data.get("description", "")
        user_hobby = UserHobbyService.add_hobby_to_user(request.user, hobby_id, description)
        return response.Response(UserHobbySerializer(user_hobby).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        UserHobbyService.delete_user_hobby(request.user, pk)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
