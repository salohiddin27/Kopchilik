from rest_framework import serializers
from .models import Group, GroupMember, UserProfile, UserChalanges


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'is_registered', 'verification_code', 'code_attempts'
                  'code_created_at', 'user_level', 'user_profession', 'total_challenges',
                  'success_rate', 'streak_days', 'location_text', 'location_private', 'email_public', 'user']
    
class UserChalangesSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='profile.user.username', read_only=True)
    email = serializers.EmailField(source='profile.email', read_only=True)
    class Meta:
        model = UserChalanges
        fields = ['id','title','description', 'location_url', 'is_active', 'total_days',
                  'days_comleted', 'username', 'email'
                  '']

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