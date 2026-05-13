from django.contrib import admin
from .models import UserProfile, Group, GroupMember
admin.site.register(UserProfile)
admin.site.register(Group)
admin.site.register(GroupMember)