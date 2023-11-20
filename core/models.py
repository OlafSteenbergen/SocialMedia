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
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png', blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    location = models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)
    
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

    def in_category(things, category):
        return things.filter(category=category)
    
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class CommentPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.user)