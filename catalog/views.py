from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Author, Book

def index (request):
    response = dict()

    PAGE_SIZE = (10,)

    all_books = Book.objects.all()
    all_authors = Author.objects.all()


    paginatior = Paginator(all_books, PAGE_SIZE[0])
    page_number = request.GET.get('page')
    page_obj = paginatior.get_page(page_number)

    response['page_title'] = 'Каталог'
    response['page'] = 'index'
    response['app'] = 'catalog'

    response['page_obj']= page_obj
    response['all_author']= all_authors

    return render(request, 'catalog/index.html', response)