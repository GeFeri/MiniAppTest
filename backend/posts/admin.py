from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html

from .models import Event, Post, Media, PostTag
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "created_by", "created_at", "image")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Превью"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "event", "uploaded_at")
    search_fields = ("title", "text")
    list_filter = ("event",)
    ordering = ("-uploaded_at",)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "media_type", "uploaded_at")
    list_filter = ("media_type",)
    search_fields = ("post__title",)

@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user")
    search_fields = ("user__username", "post__title")
