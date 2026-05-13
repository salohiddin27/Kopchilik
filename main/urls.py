from django.urls import path
from main import views
from .views import (login_view, register_view, logout_view, dashboard_view,
    GroupListCreateView, JoinGroupView, MyGroupsView)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('groups/', GroupListCreateView.as_view()),
    path('groups/<int:pk>/join/', JoinGroupView.as_view()),
    path('groups/my/', MyGroupsView.as_view()),

]