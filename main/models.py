from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile')
    email = models.EmailField(unique=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.URLField(blank=True)
    daily_goal = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateField(auto_now_add=True)
    progres = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)

    class Meta:
        unique_together = ['group', 'user']