from django.urls import path
from .views import (
    product_dashboard, product_list, product_edit, product_delete, product_add, 
    author_add, genre_add
)

urlpatterns = [
    path('', product_dashboard, name='product_dashboard'),
    path('products/', product_list, name='product_list'),
    path('products/add/', product_add, name='product_add'),
    path('products/edit/<int:book_id>/', product_edit, name='product_edit'),
    path('products/delete/<int:book_id>/', product_delete, name='product_delete'),
    
    # Додавання автора та жанру
    path('authors/add/', author_add, name='author_add'),
    path('genres/add/', genre_add, name='genre_add'),
]
