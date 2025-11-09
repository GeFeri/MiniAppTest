import uuid
from datetime import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class TypeHobby(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Hobby(models.Model):
    name = models.CharField(max_length=40)
    emoji = models.CharField(max_length=10, blank=True, null=True)
    type = models.ForeignKey(TypeHobby, on_delete=models.CASCADE, related_name='hobbies')
    color = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.emoji or ''} {self.name}"


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    tg_id = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    hobbies = models.ManyToManyField(Hobby, through='UserHobby', related_name='users')

    def __str__(self):
        return self.username


class UserHobby(models.Model):


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'hobby')  # чтобы одно хобби не дублировалось

    def __str__(self):
        return f"{self.user.username} — {self.hobby.name}"


class Department(models.Model):
    name = models.CharField(max_length=40)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_departments')

    def __str__(self):
        return self.name



class InviteKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='invites_created')
    used = models.BooleanField(default=False)
    used_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='invite_used')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    # новые поля
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        status = 'used' if self.used else 'active'
        return f"{self.key} ({status})"