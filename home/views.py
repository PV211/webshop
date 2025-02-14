from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html', {
        'page_title': 'Головна Сторінка'
    })

def contact(request):
    return render(request, 'home/contact.html', {
        'page_title': 'Контакти'
    })