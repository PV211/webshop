from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "У вас немає прав для перегляду цієї сторінки.")
            return redirect('home')  # Змінити на головну сторінку або сторінку входу
    return wrapper
