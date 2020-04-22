from functools import wraps

from django.shortcuts import redirect


def check_login(function):
    @wraps(function)
    def inner(request, *args, **kwargs):
        if request.session.get('is_login') == '1':
            return function(request, *args, **kwargs)
        else:
            return redirect('/login/')
    return inner


