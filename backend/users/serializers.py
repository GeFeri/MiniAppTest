from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import  Hobby, TypeHobby, InviteKey

from users.models import UserHobby

User = get_user_model()

# ------------------------------
# 🎨 TypeHobby
# ------------------------------
class TypeHobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeHobby
        fields = ['id', 'name']


# ------------------------------
# 🎭 Hobby
# ------------------------------
class HobbySerializer(serializers.ModelSerializer):
    type = TypeHobbySerializer(read_only=True)
    type_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Hobby
        fields = ['id', 'name', 'emoji', 'color', 'type', 'type_id']


# ⚙️ Упрощённая версия для использования в профиле пользователя
class HobbyInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name', 'emoji', 'color']


# ------------------------------
# 🧩 InviteKey
# ------------------------------
class InviteKeySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    used_by_name = serializers.CharField(source='used_by.username', read_only=True)

    class Meta:
        model = InviteKey
        fields = [
            'id', 'key', 'department', 'department_name', 'created_by', 'created_by_name',
            'first_name', 'last_name', 'telegram_username', 'used', 'used_by', 'used_by_name',
            'created_at', 'expires_at'
        ]
        read_only_fields = ['key', 'created_by', 'created_at', 'used', 'used_by']


# ------------------------------
# 👤 User (для списков / CRUD)
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    hobbies = HobbySerializer(many=True, read_only=True)
    hobbies_ids = serializers.ListField(
        write_only=True, required=False, child=serializers.IntegerField()
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'bio', 'birth_date', 'tg_id',
            'hobbies', 'hobbies_ids'
        ]
        read_only_fields = ['tg_id', 'username']


# ------------------------------
# 🎂 Для ленты дней рождений
# ------------------------------
class BirthdayUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'tg_id']

class UserHobbySerializer(serializers.ModelSerializer):
    hobby = HobbyInlineSerializer(read_only=True)
    hobby_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserHobby
        fields = ["id", "hobby", "hobby_id", "description"]
# ------------------------------
# 👤 Подробный профиль пользователя
# ------------------------------
class UserDetailSerializer(serializers.ModelSerializer):
    hobbies = UserHobbySerializer(source="userhobby_set", many=True, read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "tg_id",
            "birth_date",
            "bio",
            "avatar",
            "hobbies",
            "username"
        ]

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

