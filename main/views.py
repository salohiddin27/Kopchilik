from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json
import random
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Group, GroupMember
from .serializers import GroupSerializer, GroupMemberSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# ✅ Takrorlangan kodni oldini olish uchun helper


def parse_json(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse(
            {'success': False, 'message': 'Invalid JSON'},
            status=400
        )
# ✅ 6 xonali kod generatsiya qilish uchun helper

def generate_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    send_mail(
        subject='Tasdiqlash kodi',
        message=f'Sizning tasdiqlash kodingiz: {code}\nKod 10 daqiqa amal qiladi.',
        from_email='salohiddinnurbayev25@gmail.com',
        recipient_list=[email],
        fail_silently=False # xato bolsa exception chiqaradi
    )

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data, error = parse_json(request)
        if error:
            return error
        
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return JsonResponse(
                {'success': False, 'message': 'username, password, email kerak' },
                status=400
            )
        if User.objects.only('id').filter(username=username).exists():
            return JsonResponse(
                {'success': False, 'message': 'Username allaqachon bor'},
                status=400
            )
        
        # ✅ Kod generatsiya

        code = generate_code()

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        # ✅ is_registered=False — email tasdiqlanguncha
        UserProfile.objects.create(
            user=user,
            email=email,
            is_registered=False,
            verification_code=code,
            code_created_at=timezone.now()
        )

        # ✅ Email jo'natish — xato bo'lsa userni o'chirish
        try:
            send_verification_email(email, code)
        except Exception:
            user.delete()
            return JsonResponse(
                {'success': False, 'message': 'Email jo\'natishda xato'},
                status=500
            )
        return JsonResponse({
            'success': True,
            'message': 'kod emailga jo\'natildi, tasdiqlang'
        })

    return JsonResponse({'endpoint': '/register/', 'method': 'POST'})

@csrf_exempt
def verify_email_view(request):
    if request.method == 'POST':
        data, error = parse_json(request)
        if error:
            return error
        email = data.get('email')
        code = data.get('code')

        if not email or not code:
            return JsonResponse(
                {'success': False, 'message': 'email va code kerak'},
                status=400
            )
        try:
            profile = UserProfile.objects.only(
                'verification_code', 'is_registered',
                'code_attempts', 'code_created_at'  # ✅ yangi fieldlar qo'shildi
            ).get(email=email)
        except UserProfile.DoesNotExist:
            return JsonResponse(
                {'success': False, 'message': 'Email topilmadi'},
                status=404
            )

        if profile.is_registered:
            return JsonResponse(
                {'success': False, 'message': 'Email allaqachon tasdiqlangan'},
                status=400
            )

        # ✅ 1. Kod muddati tekshiruvi — 10 daqiqa
        from django.utils import timezone
        from datetime import timedelta
        if timezone.now() > profile.code_created_at + timedelta(minutes=10):
            return JsonResponse(
                {'success': False, 'message': 'Kod muddati o\'tdi, qayta jo\'nating'},
                status=400
            )

        # ✅ 2. Brute-force tekshiruvi — 5 ta urinish
        if profile.code_attempts >= 5:
            return JsonResponse(
                {'success': False, 'message': 'Juda ko\'p urinish, qayta ro\'yxatdan o\'ting'},
                status=429
            )

        # ✅ 3. Kod noto'g'ri — urinishni oshirish
        if profile.verification_code != code:
            profile.code_attempts += 1
            profile.save()
            return JsonResponse(
                {'success': False, 'message': f'Kod noto\'g\'ri, {5 - profile.code_attempts} urinish qoldi'},
                status=400
            )

        # ✅ 4. Hammasi to'g'ri — reset
        profile.is_registered = True
        profile.verification_code = ''
        profile.code_attempts = 0
        profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Email muvaffaqiyatli tasdiqlandi'
        })

    return JsonResponse({'endpoint': '/verify-email/', 'method': 'POST'})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data, error = parse_json(request)
        if error:
            return error
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse(
                {'success': False, 'message': 'Username va password kerak'},
                status=400
            )
        
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse(
                {'success': False, 'message': 'Username yoki parol noto\'g\'ri'},
                status=401
            )
      # ✅ Email tasdiqlanganmi tekshirish
        try:
            profile = UserProfile.objects.only('is_registered').get(user=user)
            if not profile.is_registered:
                return JsonResponse({'success': False, 'message': 'Email tasdiqlanmagan'},
                    status=403)
        except UserProfile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Profile topilmadi'},
                                status=404)
        
        login(request, user)
        return JsonResponse({'success': True, 'message': 'logged in'})
    return JsonResponse({'endpoint': '/login/', 'method': 'POST'})


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'logged out'})
    return JsonResponse({'endpoint': '/logout/', 'method': 'POST'})

class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try: 
            profile = UserProfile.objects.only(
                'email', 'is_registered'
            ).get(user=request.user)

            return Response({'success': True,
                             'username': request.user.username,
                             'email': profile.email,
                             'is_registered': profile.is_registered
                             })
        except UserProfile.DoesNotExist:
            return  Response(
                {'success': False, 'message': 'Profil topilmadi'},
                status=404 )





class GroupListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Group.objects.select_related('created_by').only(
        'id', 'name', 'description', 'cover_image',
        'daily_goal', 'created_at', 'created_by_id', 'created_by__username'
    )
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class JoinGroupView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        group = get_object_or_404(Group.objects.only('id'), pk=pk)
        member, created = GroupMember.objects.get_or_create(
            group=group, user=request.user
        )
        if created:
            return Response({'message': 'Guruhga qoshildingiz'})
        return Response({'message': 'Allaqachon azosiz'})


class MyGroupsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication] 
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupMember.objects.select_related('group', 'group__created_by').only(
            'id', 'joined_at', 'progres', 'streak', 
            'group__id', 'group__name', 'group__cover_image',
            'group__created_by__username'
        ).filter(user=self.request.user)