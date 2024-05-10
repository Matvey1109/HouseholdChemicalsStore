from django.shortcuts import redirect


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("about")

    return wrapper


def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (
            request.user.is_employee or request.user.is_superuser
        ):
            return view_func(request, *args, **kwargs)
        else:
            return redirect("about")

    return wrapper


def client_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (
            request.user.is_client or request.user.is_superuser
        ):
            return view_func(request, *args, **kwargs)
        else:
            return redirect("about")

    return wrapper
