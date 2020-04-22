from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from User.models import Users


class UserAuth(BaseAuthentication):

    def authenticate(self, request):
        if request.method == 'GET':
            token = request.query_params.get('token')
            try:
                u_id = cache.get(token)
                user = Users.objects.get(pk=u_id)
                return user, token
            except:
                return