from users.models import UserHobby, Hobby, User
from django.shortcuts import get_object_or_404

class UserHobbyService:

    @staticmethod
    def list_user_hobbies(user: User):
        return UserHobby.objects.filter(user=user).select_related("hobby")

    @staticmethod
    def add_hobby_to_user(user: User, hobby_id: int, description: str = ""):
        hobby = get_object_or_404(Hobby, id=hobby_id)
        user_hobby, created = UserHobby.objects.get_or_create(
            user=user,
            hobby=hobby,
            defaults={"description": description}
        )
        if not created:
            user_hobby.description = description
            user_hobby.save()
        return user_hobby

    @staticmethod
    def delete_user_hobby(user: User, hobby_id: int):
        UserHobby.objects.filter(user=user, hobby_id=hobby_id).delete()