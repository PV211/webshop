from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Max, Min
from django.utils.http import urlencode
from .models import *

def index(request):
    response = dict()
    per_page = request.GET.get('per_page')

    params = request.GET.copy()
    params.pop('page', None)

    all_books = Book.objects.all()
    all_authors = Author.objects.all()
    all_genres = Genre.objects.all()

    prices = all_books.aggregate(max_price = Max('price'), min_price = Min('price'))

    selected_author_ids = request.GET.getlist('authors')
    selected_genre_ids = request.GET.getlist('genres')
    current_min_price = request.GET.get('current_min_price')
    current_max_price = request.GET.get('current_max_price')
    sort = request.GET.get('sort')

    if selected_author_ids:
        selected_author_ids = list(map(int, selected_author_ids))
        all_books = all_books.filter(author__id__in=selected_author_ids).distinct()

    if selected_genre_ids:
        selected_genre_ids = list(map(int, selected_genre_ids))
        all_books = all_books.filter(genre__id__in=selected_genre_ids).distinct()

    if current_min_price:
        current_min_price = float(current_min_price)
        all_books = all_books.filter(price__gte = current_min_price)

    if current_max_price:
        current_max_price = float(current_max_price)
        all_books = all_books.filter(price__lte = current_max_price)
    
    all_books = all_books.order_by(sort if sort else "title")

    paginator = Paginator(all_books, int(per_page) if per_page else 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    response['page_title'] = 'Каталог'
    response['page_obj'] = page_obj
    response['query_params'] = urlencode(params, True)
    response['all_author'] = all_authors
    response['all_genres'] = all_genres
    response['max_price'] = prices['max_price']
    response['min_price'] = prices['min_price']

    return render(request, 'catalog/index.html', response)

def book(request, id):
    book = Book.objects.get(id = id)

    return render(request, 'catalog/book.html', {
        'page_title': book.title,
        'book': book
    })