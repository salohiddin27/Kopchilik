from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register_view, verify_email_view, login_view, logout_view, DashboardView,
    GroupListCreateView, JoinGroupView, MyGroupsView, UserProfileView, UserChalangesListView
)

router = DefaultRouter()

router.register(r'groups', GroupListCreateView, basename='group')
router.register(r'my-groups', MyGroupsView, basename='my-group')
router.register(r'user-profiles', UserProfileView, basename='user-profile')
router.register(r'user-challenges', UserChalangesListView, basename='user-challenge')

urlpatterns = [
    path('register/', register_view, name='register'),
    path('verify-email/', verify_email_view, name='verify_email'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('groups/<int:pk>/join/', JoinGroupView.as_view(), name='join_group'),

    path('', include(router.urls)),
]
#