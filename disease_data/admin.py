from django.contrib import admin
from .models import CropType, Region, ImageData, TableData, ZipData

admin.site.register(CropType)
admin.site.register(Region)
admin.site.register(ImageData)
admin.site.register(TableData)
admin.site.register(ZipData)

