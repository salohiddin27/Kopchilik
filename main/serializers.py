from rest_framework import serializers
from .models import Group, GroupMember

class GroupSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'created_by',
                 'cover_image', 'daily_goal', 'member_count'
                 ]
                 
    def get_member_count(self, obj):
        return obj.groupmember_set.count()
    
class GroupMemberSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = GroupMember
        fields = ['group', 'progres', 'streak', 'joined_at']