from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import User
from .forms import CustomUserCreationForm, ProfileForm
from disease_data.models import ImageData, TableData, ZipData
from itertools import chain

def is_admin(user):
    """检查用户是否为管理员"""
    return user.role == 'admin'

@login_required
def profile(request):
    """个人资料视图"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料更新成功！')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    # 获取用户最近上传的数据
    images = ImageData.objects.filter(uploader=request.user).order_by('-created_at')[:3]
    tables = TableData.objects.filter(uploader=request.user).order_by('-created_at')[:3]
    zips = ZipData.objects.filter(uploader=request.user).order_by('-created_at')[:3]
    
    # 合并数据并按时间排序
    recent_data = []
    for image in images:
        recent_data.append({
            'type': 'image',
            'name': image.name,
            'created_at': image.created_at,
            'url': image.image.url
        })
    
    for table in tables:
        recent_data.append({
            'type': 'table',
            'name': table.name,
            'created_at': table.created_at,
            'url': table.file.url
        })
    
    for zip_file in zips:
        recent_data.append({
            'type': 'zip',
            'name': zip_file.name,
            'created_at': zip_file.created_at,
            'url': zip_file.file.url
        })
    
    # 按时间排序
    recent_data.sort(key=lambda x: x['created_at'], reverse=True)
    recent_data = recent_data[:5]  # 只取前5条
    
    context = {
        'form': form,
        'recent_data': recent_data
    }
    
    return render(request, 'profile/index.html', context)

@login_required
@user_passes_test(is_admin)
def user_list(request):
    """用户列表视图（仅管理员可见）"""
    query = request.GET.get('q', '')
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    else:
        users = User.objects.all()
    
    # 统计用户角色数量
    admin_count = User.objects.filter(role='admin').count()
    user_count = User.objects.filter(role='user').count()
    
    context = {
        'users': users,
        'admin_count': admin_count,
        'user_count': user_count
    }
    
    return render(request, 'admin/user_list.html', context)

@login_required
@user_passes_test(is_admin)
def add_user(request):
    """添加用户视图（仅管理员可见）"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '用户添加成功！')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'admin/add_user.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    """删除用户视图（仅管理员可见）"""
    user = get_object_or_404(User, id=user_id)
    
    # 防止删除自己
    if user == request.user:
        messages.error(request, '不能删除当前登录的用户！')
        return redirect('user_list')
    
    user.delete()
    messages.success(request, '用户删除成功！')
    return redirect('user_list')

@login_required
@user_passes_test(is_admin)
def change_user_role(request, user_id):
    """修改用户角色视图（仅管理员可见）"""
    user = get_object_or_404(User, id=user_id)
    
    # 防止修改自己的角色
    if user == request.user:
        messages.error(request, '不能修改当前登录用户的角色！')
        return redirect('user_list')
    
    # 切换角色
    if user.role == 'admin':
        user.role = 'user'
        messages.success(request, f'用户 {user.username} 的角色已更新为普通用户！')
    else:
        user.role = 'admin'
        messages.success(request, f'用户 {user.username} 的角色已更新为超级管理员！')
    
    user.save()
    return redirect('user_list')

