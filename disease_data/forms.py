from django import forms
from .models import ImageData, TableData, ZipData

class ImageDataForm(forms.ModelForm):
    class Meta:
        model = ImageData
        fields = ['name', 'crop_type', 'region', 'description', 'image']
        
class TableDataForm(forms.ModelForm):
    class Meta:
        model = TableData
        fields = ['name', 'crop_type', 'region', 'description', 'file', 'source']
        
class ZipDataForm(forms.ModelForm):
    class Meta:
        model = ZipData
        fields = ['name', 'crop_type', 'region', 'description', 'file']

