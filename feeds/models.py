from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.abstract import DateTimeEntity

User = get_user_model()


# Create your models here.

class Post(DateTimeEntity):
    caption = models.CharField(max_length=500)
    image = models.ImageField(null=True, upload_to="feed_images/")
    author = models.ForeignKey(
        User, related_name='post', on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Follower(DateTimeEntity):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    being_followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='being_followeds')

    def __str__(self):
        return f'{self.follower.username, self.being_followed.username} follower-> followee'
