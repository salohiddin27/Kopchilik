from django.contrib import admin
from .models import UserProfile, Group, GroupMember, UserChalanges
admin.site.register(UserProfile)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(UserChalanges)