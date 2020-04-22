
__all__ = ['UserForm']

from django import forms
from django.contrib import auth
from django.contrib.auth.hashers import make_password

from User.models import Users, Machine


class UserForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['user_name', 'password', 'role']
        error_messages = {
            'user_name': {
                'unique': "此用户已存在"
            }
        }

    def save(self, commit=True):
        user = super().save(commit=commit)
        # user.password = auth.set_password()
        user.password = make_password(self.cleaned_data['password'], 'pbkdf2_sha1')
        user = super().save(commit=commit)
        return user


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['user_name', 'role']
        error_messages = {
            'user_name': {
                'unique': "此用户已存在"
            }
        }


class MachineForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.created_by = kwargs.pop('created_by')
    #     super().__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     instance = super().save(commit=True)
    #     instance.created_by = self.created_by
    #     if commit:
    #         instance.save()
    #     return instance

    class Meta:
        model = Machine
        fields = ['hostname', 'ip', 'port', 'account', 'password', 'platform', 'memory',
                  'disk_info', 'cpu_model', 'share_users']
        error_messages = {
            'hostname': {
                'unique': "此用户已存在"
            }
        }
        widgets = {
            'share_users': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': '用户'
            }),
        }