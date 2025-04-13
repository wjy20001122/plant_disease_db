from django.urls import path
from . import views

urlpatterns = [
    # 上传相关URL
    path('upload/image/', views.upload_image, name='upload_image'),
    path('upload/table/', views.upload_table, name='upload_table'),
    path('upload/zip/', views.upload_zip, name='upload_zip'),
    
    # 搜索相关URL
    path('search/', views.search_data, name='search_data'),
    
    # 删除相关URL
    path('delete/<str:data_type>/<int:data_id>/', views.delete_data, name='delete_data'),
]

