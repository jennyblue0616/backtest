import uuid

from django.db import models

from User.models import Users


class WorkSpace(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    file_name = models.CharField(max_length=128, unique=True)
    type = models.CharField()
    created_by = models.CharField(max_length=30, default='')
    date_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)
    last_date_updated = models.DateTimeField(verbose_name='最后更新时间', auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING, related_name='works', blank=True)


