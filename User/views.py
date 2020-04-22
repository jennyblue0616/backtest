
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from rest_framework import exceptions
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.response import Response

from User.form import UserForm, UserUpdateForm, MachineForm
from User.utils import check_login
from User.models import Users, Machine
from User.permissions import IsSuper
from User.serializers import UserSerializer


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.filter(user_name=username).first()
        if not user:
            msg = '该用户没有注册'
            return render(request, 'login.html', {'msg': msg})
        if user.is_delete:
            msg = '该账号已被冻结, 请联系管理员'
            return render(request, 'login.html', {'msg': msg})
        if check_password(password, user.password):
            request.session['is_login'] = '1'
            request.session['user_role'] = user.role
            request.session['user_id'] = user.user_name
            return HttpResponseRedirect(reverse('user:index'))
            pass
        else:
            msg = '密码错误'
            return render(request, 'login.html', {'msg': msg})


@check_login
def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return HttpResponseRedirect(reverse('user:login'))


@check_login
def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')
    if request.method == 'POST':
        old_password = request.POST.get('old_ps')
        new_password = request.POST.get('new_ps')
        new2_password = request.POST.get('new2_ps')
        user = Users.objects.filter(user_name=request.session['user_id']).first()
        if not check_password(old_password, user.password):
            msg = '原密码错误'
            return render(request, 'change_password.html', {'msg': msg})
        else:
            if old_password == new_password:
                msg = '新旧密码不能重复'
                return render(request, 'change_password.html', {'msg': msg})
            elif new_password != new2_password:
                msg = '新密码必须一致'
                return render(request, 'change_password.html', {'msg': msg})
            elif new_password == new2_password and old_password != new_password:
                user.password = make_password(new_password, 'pbkdf2_sha1')
                user.save()
                msg = '修改成功'
                return render(request, 'change_password.html', {'success_msg': msg})


@check_login
def user_state(request, *args, **kwargs):
    user = Users.objects.filter(id=kwargs['pk']).first()
    user.is_delete = 1
    user.save()
    return HttpResponseRedirect(reverse('user:user_lists'))


@method_decorator(check_login, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'


@method_decorator(check_login, name='dispatch')
class UserListView(ListView):
    template_name = 'user_list.html'
    context_object_name = 'users'
    model = Users
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': '用户管理',
            'action': '用户列表',
        })

        return context


@method_decorator(check_login, name='dispatch')
class UsersCreateView(CreateView):

    model = Users
    template_name = 'user_create_update.html'
    form_class = UserForm
    success_url = reverse_lazy('user:user_lists')

    def get_context_data(self, **kwargs):
        context = {
            'app': '用户',
            'action': '新增用户',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


@method_decorator(check_login, name='dispatch')
class UserUpdateView(UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = 'user_create_update.html'
    success_url = reverse_lazy('user:user_lists')

    def get_context_data(self, **kwargs):
        context = {
            'app': '用户管理',
            'action': '更新用户',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


@method_decorator(check_login, name='dispatch')
class MachineListView(ListView):
    template_name = 'machine_list.html'
    context_object_name = 'machines_list'
    model = Machine
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': '用户',
            'action': '算力列表',
        })

        return context


@method_decorator(check_login, name='dispatch')
class MachineCreateView(CreateView):
    template_name = 'machine_create_update.html'
    model = Machine
    form_class = MachineForm
    success_url = reverse_lazy('user:machine_list')

    def get_context_data(self, **kwargs):
        context = {
            'app': '用户',
            'action': '新增算力',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        machine = form.save(commit=False)
        machine.created_by = self.request.session['user_id'] or 'System'
        machine.save()
        return super().form_valid(form)

    # def get_form_kwargs(self):
    #     #     kwargs = super().get_form_kwargs()
    #     #     print(self.request.user)
    #     #     kwargs.update({
    #     #         'created_by': self.request.session['user_id']
    #     #     })
    #     #     return kwargs


@method_decorator(check_login, name='dispatch')
class MachineUpdateView(UpdateView):
    model = Machine
    form_class = MachineForm
    template_name = 'machine_create_update.html'
    success_url = reverse_lazy('user:machine_list')

    def get_context_data(self, **kwargs):
        context = {
            'app': '用户',
            'action': '更新算力',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


