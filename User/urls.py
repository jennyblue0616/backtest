from django.conf.urls import url
from django.urls import path

from User import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('user_list/', views.UserListView.as_view(), name='user_lists'),
    path('user_create/', views.UsersCreateView.as_view(), name='user_create'),
    path('user_create/<uuid:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_state/<uuid:pk>', views.user_state, name='user_state'),
    path('machine_list/', views.MachineListView.as_view(), name='machine_list'),
    path('machine_create/', views.MachineCreateView.as_view(), name='machine_create'),
    path('machine_create/<uuid:pk>', views.MachineUpdateView.as_view(), name='machine_update'),

]