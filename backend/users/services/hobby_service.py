# backend/users/services/hobby_service.py
from users.models import Hobby, TypeHobby

class HobbyService:
    @staticmethod
    def list_hobbies():
        return Hobby.objects.select_related('type').all()

    @staticmethod
    def create_hobby(name: str, emoji: str, color: str, type_id: int):
        return Hobby.objects.create(
            name=name,
            emoji=emoji,
            color=color,
            type_id=type_id
        )

    @staticmethod
    def delete_hobby(hobby_id: int):
        Hobby.objects.filter(id=hobby_id).delete()
