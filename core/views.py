from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from disease_data.models import ImageData, TableData, ZipData, CropType, Region
from users.models import User
from django.db.models import Count

@login_required
def dashboard(request):
    """仪表盘视图"""
    # 获取数据统计
    images_count = ImageData.objects.count()
    tables_count = TableData.objects.count()
    zips_count = ZipData.objects.count()
    
    # 获取最近上传的数据
    recent_images = ImageData.objects.order_by('-created_at')[:5]
    recent_tables = TableData.objects.order_by('-created_at')[:5]
    recent_zips = ZipData.objects.order_by('-created_at')[:5]
    
    # 获取筛选选项
    crop_types = CropType.objects.all()
    users = User.objects.all()
    
    context = {
        'images_count': images_count,
        'tables_count': tables_count,
        'zips_count': zips_count,
        'recent_images': recent_images,
        'recent_tables': recent_tables,
        'recent_zips': recent_zips,
        'crop_types': crop_types,
        'users': users,
    }
    
    return render(request, 'dashboard/index.html', context)

