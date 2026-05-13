from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Group, GroupMember
from .serializers import GroupSerializer, GroupMemberSerializer


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Logged in'})
        return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'endpoint': '/login/', 'method': 'POST'})


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if not username or not password or not email:
            return JsonResponse({'success': False, 'message': 'username, password, email required'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists'}, status=400)
        if UserProfile.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already exists'}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user, email=email, is_registered=True)
        return JsonResponse({'success': True, 'message': 'Registered successfully'})
    return JsonResponse({'endpoint': '/register/', 'method': 'POST'})


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logged out'})
    return JsonResponse({'endpoint': '/logout/', 'method': 'POST'})


def dashboard_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Not authenticated'}, status=401)
    try:
        profile = request.user.UserProfile
        return JsonResponse({
            'success': True,
            'username': request.user.username,
            'email': profile.email,
            'is_registered': profile.is_registered
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Profile not found'}, status=404)


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        group = Group.objects.get(pk=pk)
        member, created = GroupMember.objects.get_or_create(
            group=group, user=request.user
        )
        if created:
            return Response({'message': 'Guruhga qoshildingiz'})
        return Response({'message': 'Allaqachon azosiz'})


class MyGroupsView(generics.ListAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupMember.objects.filter(user=self.request.user)