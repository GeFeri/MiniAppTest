# backend/users/services/user_service.py
from datetime import date

from aiogram import F
from django.db.models import ExpressionWrapper
from rest_framework.generics import get_object_or_404
from users.models import Hobby
from django.contrib.auth import get_user_model
User = get_user_model()
class UserService:
    @staticmethod
    def get_by_telegram_id(tg_id: int):
        return User.objects.get(tg_id=tg_id)

    @staticmethod
    def list_users():
        return User.objects.all()

    @staticmethod
    def update_profile(user: User, bio=None, birth_date=None, hobbies_ids=None):
        if bio is not None:
            user.bio = bio
        if birth_date is not None:
            user.birth_date = birth_date
        user.save()

        if hobbies_ids is not None:
            user.hobbies.set(Hobby.objects.filter(id__in=hobbies_ids))

        return user

    @staticmethod
    def list_birthdays(limit: int = 30):
        """
        Возвращает пользователей, у которых день рождения в ближайшие `limit` дней.
        Работает корректно при переходе через Новый Год.
        """
        today = date.today()
        upcoming = []

        for user in User.objects.filter(birth_date__isnull=False):
            bd = user.birth_date

            # день рождения в этом году
            next_bd = bd.replace(year=today.year)

            # если уже прошёл — переносим на следующий год
            if next_bd < today:
                next_bd = bd.replace(year=today.year + 1)

            days_left = (next_bd - today).days
            upcoming.append((days_left, user))

        # сортируем по ближайшему
        upcoming.sort(key=lambda x: x[0])
        return [u for _, u in upcoming[:limit]]

    @staticmethod
    def get_user_detail(user_id: int) -> User:
        """
        Возвращает одного пользователя по ID (для детального просмотра профиля).
        """
        return get_object_or_404(User, id=user_id)