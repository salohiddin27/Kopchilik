from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile')
    email = models.EmailField(unique=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
