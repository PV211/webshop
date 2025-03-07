from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.http import urlencode
from catalog.models import Book
from .models import FavouriteItem
from django.contrib.auth.decorators import login_required

@login_required(login_url = "/login")
def index(request):
    per_page = request.GET.get('per_page')

    params = request.GET.copy()
    params.pop('page', None)

    favourite_items = FavouriteItem.objects.filter(user = request.user)

    sort = request.GET.get('sort')
    
    favourite_items = favourite_items.order_by(sort if sort else "book__title")

    paginator = Paginator(favourite_items, int(per_page) if per_page else 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'favourites/index.html', {
        'page_title': 'Обрані книги',
        'page_obj': page_obj,
        'query_params': urlencode(params, True)
    })

def add(request, id):
    book = Book.objects.get(id = id)
    user = request.user

    if book:
        if not FavouriteItem.objects.filter(book = book, user = user).exists():
            FavouriteItem.objects.create(
                book = book,
                user = user
            )

            messages.success(request, "Книга додана до обраних")
        else:
            messages.error(request, 'Помилка, книга вже в обраних')
    else:
        messages.error(request, 'Помилка, книга не знайдена')
    
    return JsonResponse({"success": True})

def remove(request, id):
    FavouriteItem.objects.get(id = id).delete()

    messages.success(request, 'Книга видалена з обраних')

    return JsonResponse({"success": True})

def count(request):
    favourite_items = FavouriteItem.objects.filter(user = request.user)

    return JsonResponse({"success": True, 'count': len(favourite_items)})