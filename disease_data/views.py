from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ImageData, TableData, ZipData, CropType, Region
from .forms import ImageDataForm, TableDataForm, ZipDataForm
from users.models import User

@login_required
def upload_image(request):
    """上传图片视图"""
    if request.method == 'POST':
        form = ImageDataForm(request.POST, request.FILES)
        if form.is_valid():
            image_data = form.save(commit=False)
            image_data.uploader = request.user
            image_data.save()
            messages.success(request, '图片上传成功！')
            return redirect('dashboard')
    else:
        form = ImageDataForm()
    
    return render(request, 'upload/image.html', {'form': form})

@login_required
def upload_table(request):
    """上传表格视图"""
    if request.method == 'POST':
        form = TableDataForm(request.POST, request.FILES)
        if form.is_valid():
            table_data = form.save(commit=False)
            table_data.uploader = request.user
            table_data.save()
            messages.success(request, '表格上传成功！')
            return redirect('dashboard')
    else:
        form = TableDataForm()
    
    return render(request, 'upload/table.html', {'form': form})

@login_required
def upload_zip(request):
    """上传ZIP文件视图"""
    if request.method == 'POST':
        form = ZipDataForm(request.POST, request.FILES)
        if form.is_valid():
            zip_data = form.save(commit=False)
            zip_data.uploader = request.user
            zip_data.save()
            messages.success(request, 'ZIP文件上传成功！')
            return redirect('dashboard')
    else:
        form = ZipDataForm()
    
    return render(request, 'upload/zip.html', {'form': form})

@login_required
def search_data(request):
    """搜索数据视图"""
    query = request.GET.get('q', '')
    crop_type = request.GET.get('crop_type', '')
    region = request.GET.get('region', '')
    uploader = request.GET.get('uploader', '')
    data_type = request.GET.get('type', '')
    
    # 初始化查询集
    images = ImageData.objects.all()
    tables = TableData.objects.all()
    zips = ZipData.objects.all()
    
    # 应用搜索条件
    if query:
        images = images.filter(Q(name__icontains=query) | Q(description__icontains=query))
        tables = tables.filter(Q(name__icontains=query) | Q(description__icontains=query))
        zips = zips.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if crop_type:
        images = images.filter(crop_type__name=crop_type)
        tables = tables.filter(crop_type__name=crop_type)
        zips = zips.filter(crop_type__name=crop_type)
    
    if region:
        images = images.filter(region__name=region)
        tables = tables.filter(region__name=region)
        zips = zips.filter(region__name=region)
    
    if uploader:
        images = images.filter(uploader__username=uploader)
        tables = tables.filter(uploader__username=uploader)
        zips = zips.filter(uploader__username=uploader)
    
    # 根据数据类型筛选
    if data_type == 'image':
        tables = TableData.objects.none()
        zips = ZipData.objects.none()
    elif data_type == 'table':
        images = ImageData.objects.none()
        zips = ZipData.objects.none()
    elif data_type == 'zip':
        images = ImageData.objects.none()
        tables = TableData.objects.none()
    
    # 获取筛选选项
    crop_types = CropType.objects.all()
    regions = Region.objects.all()
    users = User.objects.all()
    
    context = {
        'query': query,
        'crop_type': crop_type,
        'region': region,
        'uploader': uploader,
        'images': images,
        'tables': tables,
        'zips': zips,
        'crop_types': crop_types,
        'regions': regions,
        'users': users,
    }
    
    return render(request, 'dashboard/search.html', context)

@login_required
def delete_data(request, data_type, data_id):
    """删除数据视图"""
    if data_type == 'image':
        data = get_object_or_404(ImageData, id=data_id)
    elif data_type == 'table':
        data = get_object_or_404(TableData, id=data_id)
    elif data_type == 'zip':
        data = get_object_or_404(ZipData, id=data_id)
    else:
        messages.error(request, '无效的数据类型！')
        return redirect('dashboard')
    
    # 检查权限
    if request.user.role == 'admin' or data.uploader == request.user:
        data.delete()
        messages.success(request, '数据删除成功！')
    else:
        messages.error(request, '您没有权限删除此数据！')
    
    # 返回到之前的页面
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('dashboard')

