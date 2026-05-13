from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import UserProfile

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
    
    return JsonResponse({
        'endpoint': '/login/',
        'method': 'POST',
        'body': {'username': 'your_username', 'password': 'your_password'}
    })


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

    return JsonResponse({
        'endpoint': '/register/',
        'method': 'POST',
        'body': {'username': 'your_username', 'password': 'your_password', 'email': 'your_email'}
    })


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