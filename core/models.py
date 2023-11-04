from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime, timezone

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
    @property
    def days_ago(self):
        hours_ago = round((datetime.now(timezone.utc) - self.created_at).total_seconds() / 3600 + 1)
        minutes_ago = round((datetime.now(timezone.utc) - self.created_at).total_seconds() / 60)
        if hours_ago < 1:
            return str(minutes_ago + 60) + ' minutes ago'
        elif hours_ago == 1:
              return str(hours_ago) + ' hour ago'          
        elif hours_ago < 24:
            return str(hours_ago) + ' hours ago'
        elif hours_ago < 48:
            return str(round(hours_ago / 24)) + ' day ago'
        else:
            return str(round(hours_ago / 24)) + ' days ago'

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user