from django.contrib.auth.decorators import login_required, user_passes_test


def group_required(group_name):
    def decorator(view_func):
        @login_required
        @user_passes_test(lambda user: user.groups.filter(name=group_name).exists() or user.is_staff, login_url='login')
        def wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
