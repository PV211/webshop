from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Max, Min
from .models import *

def index(request):
    response = dict()
    PAGE_SIZE = 4

    all_books = Book.objects.all()
    all_authors = Author.objects.all()
    all_genres = Genre.objects.all()

    max_price = all_books.aggregate(Max('price'))['price__max']
    min_price = all_books.aggregate(Min('price'))['price__min']

    # Отримуємо вибрані автори з GET-запиту
    selected_author_ids = list(map(int, request.GET.getlist('authors')))
    selected_genre_ids = list(map(int, request.GET.getlist('genres')))
    if selected_author_ids:
        all_books = all_books.filter(author__id__in=selected_author_ids).distinct()
    if selected_genre_ids:
        all_books = all_books.filter(genre__id__in=selected_genre_ids).distinct()

    paginator = Paginator(all_books, PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    response['page_title'] = 'Каталог'
    response['page_obj'] = page_obj
    response['all_author'] = all_authors
    response['all_genres'] = all_genres
    response['max_price'] = max_price
    response['min_price'] = min_price

    return render(request, 'catalog/index.html', response)