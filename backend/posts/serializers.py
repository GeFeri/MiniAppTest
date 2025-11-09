from rest_framework import serializers
from posts.models import Event, Post, Media, PostTag
from users.serializers import UserSerializer
from users.models import User

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Event
        fields = ['id','title','content','date','created_by','created_at','image']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id','file','media_type','uploaded_at']

class PostTagSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PostTag
        fields = ['id','user','user_id']

class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)
    tags = PostTagSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id','title','text','event','author','uploaded_at','media','tags']

class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    text = serializers.CharField(allow_blank=True, required=False)
    event_id = serializers.IntegerField()
    tagged_users = serializers.ListField(child=serializers.IntegerField(), required=False)
    # media_files come via request.FILES
    media_types = serializers.ListField(child=serializers.ChoiceField(choices=[("photo","Photo"),("video","Video")]), required=False)

    def validate(self, data):
        # validation of event existence moved to view/service
        return data
