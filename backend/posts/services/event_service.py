# backend/posts/services/event_service.py
from posts.models import Event
from django.contrib.auth import get_user_model
User = get_user_model()

class EventService:
    @staticmethod
    def create_event(title: str, content: str, date, created_by: User):
        return Event.objects.create(
            title=title,
            content=content,
            date=date,
            created_by=created_by
        )

    @staticmethod
    def update_event(event_id: int, title=None, content=None, date=None):
        event = Event.objects.get(id=event_id)
        if title is not None:
            event.title = title
        if content is not None:
            event.content = content
        if date is not None:
            event.date = date
        event.save()
        return event

    @staticmethod
    def delete_event(event_id: int):
        Event.objects.filter(id=event_id).delete()

    @staticmethod
    def get_event_detail(event_id: int):
        return Event.objects.prefetch_related('posts').get(id=event_id)

    @staticmethod
    def list_events():
        return Event.objects.all().order_by('-date')
