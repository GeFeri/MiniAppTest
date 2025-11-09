# backend/posts/views/event_view.py
from rest_framework import viewsets, permissions, response, status
from posts.services.event_service import EventService
from posts.serializers import EventSerializer

class EventViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        events = EventService.list_events()
        return response.Response(EventSerializer(events, many=True).data)

    def retrieve(self, request, pk=None):
        event = EventService.get_event_detail(pk)
        return response.Response(EventSerializer(event).data)

    def create(self, request):
        event = EventService.create_event(
            title=request.data.get('title'),
            content=request.data.get('content'),
            date=request.data.get('date'),
            created_by=request.user
        )
        return response.Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        event = EventService.update_event(
            pk,
            title=request.data.get('title'),
            content=request.data.get('content'),
            date=request.data.get('date')
        )
        return response.Response(EventSerializer(event).data)

    def destroy(self, request, pk=None):
        EventService.delete_event(pk)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
