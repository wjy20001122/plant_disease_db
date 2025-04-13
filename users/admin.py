from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'phone', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('自定义字段', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('自定义字段', {'fields': ('role', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)

