from rest_framework.permissions import BasePermission

from User.models import Users


class IsSuper(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            if isinstance(request.user, Users):
                # request.user.is_super 是超级管理员值为True
                return request.user
            return False
        return True



