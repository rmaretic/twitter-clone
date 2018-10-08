from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now())

    def __str__(self):
        title = (self.post[:10] + '...') if len(self.post) > 10 else self.post
        return title


class Follower(models.Model):
    base_user = models.ForeignKey(User, related_name='base', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.base_user.username + ' follows ' + self.followed.username
