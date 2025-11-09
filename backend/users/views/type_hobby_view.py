# users/views/type_hobby_view.py
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import TypeHobby
from users.serializers import TypeHobbySerializer

class TypeHobbyViewSet(ReadOnlyModelViewSet):
    """
    API для получения списка типов хобби (категорий)
    GET /api/type-hobbies/
    GET /api/type-hobbies/{id}/
    """
    queryset = TypeHobby.objects.all().order_by("id")
    serializer_class = TypeHobbySerializer
    permission_classes = []  # AllowAny для теста
