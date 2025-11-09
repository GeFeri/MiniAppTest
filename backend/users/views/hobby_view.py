# backend/users/views/hobby_view.py
from rest_framework import viewsets, permissions, response, status
from users.services.hobby_service import HobbyService
from users.serializers import HobbySerializer

class HobbyViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        hobbies = HobbyService.list_hobbies()
        return response.Response(HobbySerializer(hobbies, many=True).data)

    def create(self, request):
        hobby = HobbyService.create_hobby(
            name=request.data.get('name'),
            emoji=request.data.get('emoji'),
            color=request.data.get('color'),
            type_id=request.data.get('type_id')
        )
        return response.Response(HobbySerializer(hobby).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        hobby = HobbyService.get_hobby(pk)
        return response.Response(HobbySerializer(hobby).data)

    def update(self, request, pk=None):
        hobby = HobbyService.update_hobby(
            hobby_id=pk,
            name=request.data.get('name'),
            emoji=request.data.get('emoji'),
            color=request.data.get('color'),
            type_id=request.data.get('type_id')
        )
        return response.Response(HobbySerializer(hobby).data)

    def destroy(self, request, pk=None):
        HobbyService.delete_hobby(pk)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
