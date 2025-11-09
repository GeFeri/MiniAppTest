from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from posts.services.post_service import PostService
from posts.serializers import PostSerializer, PostCreateSerializer

class PostViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # support query params: ?type=event&event_id=... or ?type=media
        t = request.query_params.get('type')
        if t == 'event':
            event_id = request.query_params.get('event_id')
            if not event_id:
                return Response({'error':'event_id required for type=event'}, status=400)
            posts = PostService.get_event_feed(event_id)
        else:
            posts = PostService.get_media_feed()
        return Response(PostSerializer(posts, many=True).data)

    def retrieve(self, request, pk=None):
        post = PostService.get_post_detail(pk)
        return Response(PostSerializer(post).data)

    def create(self, request):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        media_files = request.FILES.getlist('files')
        media_types = request.data.getlist('media_types')
        tagged_users = request.data.getlist('tagged_users')

        # basic length check
        if media_files and len(media_files) != len(media_types):
            return Response({'error':'media_types length must match files'}, status=400)

        post = PostService.create_post(
            author=request.user,
            title=serializer.validated_data['title'],
            text=serializer.validated_data.get('text',''),
            event_id=serializer.validated_data['event_id'],
            media_files=media_files,
            media_types=media_types,
            tagged_users=[int(x) for x in tagged_users] if tagged_users else []
        )
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        post = PostService.update_post(pk, title=request.data.get('title'), text=request.data.get('text'))
        return Response(PostSerializer(post).data)

    def destroy(self, request, pk=None):
        PostService.delete_post(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
