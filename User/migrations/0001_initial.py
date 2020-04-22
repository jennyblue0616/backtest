# Generated by Django 3.0.5 on 2020-04-20 06:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=64, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('role', models.IntegerField(choices=[(1, '普通用户'), (2, '管理员')], default=1, verbose_name='角色')),
                ('is_delete', models.BooleanField(default=False, verbose_name='状态')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '用户管理',
            },
        ),
    ]