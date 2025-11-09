# backend/posts/services/post_service.py
from typing import List
from django.db import transaction
from posts.models import Event, Post, Media, PostTag
from django.contrib.auth import get_user_model
User = get_user_model()

class PostService:
    @staticmethod
    @transaction.atomic
    def create_post(author: User, title: str, text: str, event_id: int, media_files: List, media_types: List[str], tagged_users: List[int]):
        event = Event.objects.get(id=event_id)
        post = Post.objects.create(
            title=title,
            text=text,
            event=event
        )
        for file_obj, mtype in zip(media_files, media_types):
            Media.objects.create(
                post=post,
                file=file_obj,
                media_type=mtype
            )
        for user_id in tagged_users:
            tagged_user = User.objects.get(id=user_id)
            PostTag.objects.create(post=post, user=tagged_user)
        return post

    @staticmethod
    def update_post(post_id: int, title=None, text=None):
        post = Post.objects.get(id=post_id)
        if title is not None:
            post.title = title
        if text is not None:
            post.text = text
        post.save()
        return post

    @staticmethod
    def delete_post(post_id: int):
        Post.objects.filter(id=post_id).delete()

    @staticmethod
    def get_post_detail(post_id: int):
        return Post.objects.prefetch_related('media', 'tags', 'tags__user').get(id=post_id)

    @staticmethod
    def get_event_feed(event_id: int):
        return Post.objects.filter(event_id=event_id).prefetch_related('media', 'tags', 'tags__user')

    @staticmethod
    def get_media_feed():
        return Post.objects.filter(media__isnull=False).distinct().prefetch_related('media', 'tags', 'tags__user')
