# backend/users/services/invite_service.py
import uuid
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import InviteKey
from django.contrib.auth import get_user_model
User = get_user_model()


class InviteService:
    @staticmethod
    def create_invite(created_by: User, department, first_name: str, last_name: str, telegram_username: str = None, expires_in_hours: int = 48):
        return InviteKey.objects.create(
            department=department,
            created_by=created_by,
            first_name=first_name,
            last_name=last_name,
            telegram_username=telegram_username,
            expires_at=timezone.now() + timedelta(hours=expires_in_hours)
        )

    @staticmethod
    def activate_invite(telegram_id: int, input_key: str):
        existing_user = User.objects.filter(tg_id=telegram_id).first()
        if existing_user:
            return existing_user

        try:
            invite = InviteKey.objects.get(key=input_key, used=False)
        except InviteKey.DoesNotExist:
            raise ValidationError("Неверный или использованный ключ")

        if invite.expires_at and invite.expires_at < timezone.now():
            raise ValidationError("Ключ просрочен")

        user = User.objects.create(
            username=f"user_{telegram_id}",
            first_name=invite.first_name,
            last_name=invite.last_name,
            tg_id=telegram_id,
        )

        invite.used = True
        invite.used_by = user
        invite.save()
        return user

    @staticmethod
    def list_invites():
        return InviteKey.objects.all()

    @staticmethod
    def get_invite_detail(invite_id):
        return InviteKey.objects.get(id=invite_id)

    @staticmethod
    def delete_invite(invite_id):
        InviteKey.objects.filter(id=invite_id).delete()
