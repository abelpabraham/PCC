from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauthenticated_user(func1):
    def wrap_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('../dashboard')
        else:
            return func1(request, *args, **kwargs)
    return wrap_func

def allowed_users( allowed_roles=[]):
    def decorator(view_func):
        def wrap_func(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorised to visit this page.")
                
        return wrap_func
    return decorator


def admin_only(view_func):
    def wrap_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'guest':
            return redirect('userhome')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrap_func