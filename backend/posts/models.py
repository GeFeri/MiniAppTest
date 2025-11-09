from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Event(models.Model):
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=60)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.id})"


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="media/posts/")
    media_type = models.CharField(
        max_length=10,
        choices=[("photo", "Photo"), ("video", "Video")]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for Post {self.post.id}"


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tags")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tagged_in")

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user} tagged in Post {self.post.id}"

