from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    User, TypeHobby, Hobby, UserHobby,
    Department, InviteKey
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "tg_id", "birth_date", "avatar")
    readonly_fields = ("avatar_preview",)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;" />', obj.avatar.url)
        return "-"
    avatar_preview.short_description = "Аватар"

@admin.register(TypeHobby)
class TypeHobbyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "emoji", "color", "type")
    list_filter = ("type",)
    search_fields = ("name",)

@admin.register(UserHobby)
class UserHobbyAdmin(admin.ModelAdmin):
    list_display = ("user", "hobby", "description")
    list_filter = ("hobby",)
    search_fields = ("user__username", "hobby__name")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "manager")
    search_fields = ("name", "manager__username")

@admin.register(InviteKey)
class InviteKeyAdmin(admin.ModelAdmin):
    list_display = (
        "key", "department", "created_by",
        "used", "used_by", "created_at", "expires_at"
    )
    list_filter = ("used", "department", "created_at")
    search_fields = ("key", "created_by__username", "used_by__username")
    readonly_fields = ("key", "created_at")
