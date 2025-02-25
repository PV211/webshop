from django.shortcuts import render

def index(request):
    return render(request, 'cart/index.html', {
        'page_title': 'Кошик'
    })