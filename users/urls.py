from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 认证相关URL
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='/users/password_change_done/'
    ), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),
    
    # 个人资料
    path('profile/', views.profile, name='profile'),
    
    # 用户管理（仅管理员可见）
    path('list/', views.user_list, name='user_list'),
    path('add/', views.add_user, name='add_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('change-role/<int:user_id>/', views.change_user_role, name='change_user_role'),
]

