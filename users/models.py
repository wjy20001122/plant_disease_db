from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """自定义用户模型"""
    ROLE_CHOICES = (
        ('admin', '超级管理员'),
        ('user', '普通用户'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="用户角色")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="联系电话")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)