from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    return render(request, 'home/index.html', {
        'page_title': 'Головна Сторінка'
    })

def contact(request):
    return render(request, 'home/contact.html', {
        'page_title': 'Контакти'
    })

def signin(request):
    context = dict()
    context['page_title'] = 'Вхід'

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username = name, email = email, password = password)

        if user:
            login(request, user)
            messages.success(request, 'Авторизація успішна!')

            return redirect('/')
        else:
            messages.error(request, 'Сталася помилка під час авторизації')

    return render(request, 'home/login.html', context)

def register(request):
    context = dict()
    context['page_title'] = 'Реєстрація'

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            user = User.objects.create_user(name, email, password)

            if user:
                login(request, user)
                messages.success(request, 'Обліковий запис створено!')

                return redirect('/')
            else:
                messages.error(request, 'Сталася помилка під час реєстрації')
        else:
            messages.error(request, 'паролі не збігаються')

    return render(request, 'home/register.html', context)

def signout(request):
    logout(request)
    messages.success(request, 'Вихід успішний!')

    return redirect('/')