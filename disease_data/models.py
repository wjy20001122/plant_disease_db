from django.db import models
from core.models import BaseModel
from users.models import User

class CropType(models.Model):
    """作物类型"""
    name = models.CharField(max_length=50, unique=True, verbose_name="作物名称")
    
    class Meta:
        verbose_name = "作物类型"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

class Region(models.Model):
    """地区信息"""
    name = models.CharField(max_length=100, unique=True, verbose_name="地区名称")
    
    class Meta:
        verbose_name = "地区"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

class BaseData(BaseModel):
    """所有数据的基类"""
    name = models.CharField(max_length=200, verbose_name="名称")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="上传者")
    crop_type = models.ForeignKey(CropType, on_delete=models.CASCADE, verbose_name="作物类型")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="地区")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    
    class Meta:
        abstract = True

class ImageData(BaseData):
    """图片数据"""
    image = models.ImageField(upload_to='images/', verbose_name="图片")
    
    class Meta:
        verbose_name = "图片数据"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

class TableData(BaseData):
    """表格数据"""
    file = models.FileField(upload_to='tables/', verbose_name="表格文件")
    source = models.CharField(max_length=200, blank=True, null=True, verbose_name="数据来源")
    
    class Meta:
        verbose_name = "表格数据"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

class ZipData(BaseData):
    """ZIP文件数据"""
    file = models.FileField(upload_to='zips/', verbose_name="ZIP文件")
    
    class Meta:
        verbose_name = "ZIP文件数据"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

