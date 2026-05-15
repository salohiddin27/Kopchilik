from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile')
    email = models.EmailField(unique=True)
    is_registered = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True)
    code_attempts = models.IntegerField(default=0) 
    code_created_at = models.DateTimeField(null=True, blank=True)

    user_level = models.IntegerField(default=1, help_text="User level 12")
    user_profession = models.CharField(max_length=20, blank=True, help_text="User profession (Programer)")

    total_challenges = models.IntegerField(default=0, help_text="Number of Chaqiriqlar")
    success_rate = models.IntegerField(default=0, help_text="Success Rate Percentage (92%)")
    streak_days = models.IntegerField(default=0, help_text="Streak Days (12)")
    location_text = models.CharField(max_length=200, blank=True, help_text="Location (Tashkent, Uzbekistan)")
    location_private = models.BooleanField(default=True, help_text="Is location private?")
    email_public = models.BooleanField(default=True, help_text="is email public?")



    def __str__(self):
        return f"{self.user.username}'s Profile"

class UserChalanges(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="challanges")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location_url = models.URLField(max_length=500, blank=True, null=True, help_text="Google Maps yoki havola linki")
    is_active = models.BooleanField(default=True)
    total_days = models.IntegerField(default=30)
    days_completed = models.IntegerField(default=0)

    def __str__(self):
        return self.title

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
    joined_at = models.DateTimeField(auto_now_add=True)
    progres = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)

    class Meta:
        unique_together = ['group', 'user']