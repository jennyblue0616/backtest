import uuid

from django.db import models


class Users(models.Model):
    ROLE_CHOICES = (
        (1, '普通用户'),
        (2, '管理员'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user_name = models.CharField(verbose_name='用户名', max_length=64, unique=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    role = models.IntegerField(verbose_name='角色', choices=ROLE_CHOICES, default=1)
    is_delete = models.BooleanField(verbose_name='状态', default=False)
    date_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = '用户管理'


class Machine(models.Model):
    PLATFORM_CHOICES = (
        ('Centos', 'Centos'),
        ('Windows', 'Windows'),
    )
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    hostname = models.CharField(max_length=128, verbose_name='主机名', unique=True)
    ip = models.GenericIPAddressField(max_length=32, verbose_name='IP')
    port = models.IntegerField(verbose_name='端口')
    account = models.CharField(verbose_name='用户名', max_length=64)
    password = models.CharField(verbose_name='密码', max_length=256)
    platform = models.CharField(max_length=128, choices=PLATFORM_CHOICES, verbose_name='操作系统')
    memory = models.CharField(max_length=64, null=True, blank=True, verbose_name='内存')
    disk_info = models.CharField(max_length=1024, null=True, blank=True, verbose_name='硬盘')
    cpu_model = models.CharField(max_length=128, null=True, blank=True, verbose_name='CPU')
    share_users = models.ManyToManyField('User.Users', blank=True, related_name='machines', verbose_name="分配用户")

    created_by = models.CharField(max_length=32, null=True, blank=True, verbose_name='创建人')
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')







