from rest_framework import viewsets, permissions, decorators, response, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from users.serializers import UserSerializer, UserDetailSerializer
from users.services.user_service import UserService

User = get_user_model()

class UserViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = UserService.list_users()
        serializer = UserSerializer(queryset, many=True, context={"request": request})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Подробный профиль пользователя"""
        user = UserService.get_user_detail(pk)
        serializer = UserDetailSerializer(user, context={"request": request})  # 👈 добавили контекст
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        if user != request.user and not request.user.is_staff:
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        updated = UserService.update_profile(
            user=user,
            bio=request.data.get("bio"),
            birth_date=request.data.get("birth_date"),
            hobbies_ids=request.data.get("hobbies_ids"),
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
        )
        return response.Response(UserSerializer(updated, context={"request": request}).data)

    @decorators.action(detail=False, methods=["get"])
    def me(self, request):
        """Профиль текущего пользователя"""
        serializer = UserSerializer(request.user, context={"request": request})
        return response.Response(serializer.data)
