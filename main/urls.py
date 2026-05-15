from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    login_view, register_view, logout_view, verify_email_view,
    DashboardView, GroupListCreateView, JoinGroupView, MyGroupsView,
    UserProfileView, UserChalangesListView
)

router = DefaultRouter()

router.register(r'profiles', UserProfileView, basename='profiles')
router.register(r'challenges', UserChalangesListView, basename='challenges')

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('verify-email/', verify_email_view, name='verify-email'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('groups/', GroupListCreateView.as_view(), name='groups'),
    path('groups/<int:pk>/join/', JoinGroupView.as_view(), name='join-group'),
    path('groups/my/', MyGroupsView.as_view(), name='my-groups'),

    path('', include(router.urls)),
]