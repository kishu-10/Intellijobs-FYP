from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.abstract import DateTimeEntity

User = get_user_model()


# Create your models here.

class Post(DateTimeEntity):
    caption = models.CharField()
    author = models.ForeignKey(
        User, related_name='post', on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class PostImage(DateTimeEntity):
    post = models.ForeignKey(
        Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')


class Like(DateTimeEntity):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liker')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')


class Comment(DateTimeEntity):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=500, blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commenter')

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
