from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Author, Book

def index(request):
    response = dict()
    PAGE_SIZE = 3

    all_books = Book.objects.all()
    all_authors = Author.objects.all()

    # Отримуємо вибрані автори з GET-запиту
    selected_authors_ids = request.GET.getlist('authors')
    if selected_authors_ids:
        all_books = all_books.filter(author__id__in=selected_authors_ids).distinct()

    paginator = Paginator(all_books, PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    response['page_title'] = 'Каталог'
    response['page'] = 'index'
    response['app'] = 'catalog'
    response['page_obj'] = page_obj
    response['all_author'] = all_authors

    return render(request, 'catalog/index.html', response)