from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from catalog.models import Book
from .models import CartItem

def index(request):
    cart_items = CartItem.objects.filter(user__id = request.user.id)

    return render(request, 'cart/index.html', {
        'page_title': 'Кошик',
        'cart_items': cart_items
    })

def checkout(request):
    cart_items = CartItem.objects.filter(user__id = request.user.id)

    return render(request, 'cart/checkout.html', {
        'page_title': 'Адреса Доставки',
        'cart_items': cart_items
    })

def add(request, id):
    book = Book.objects.get(id = id)

    if book:
        CartItem.objects.create(
            book = book,
            user = request.user
        )

        messages.success(request, "Книга додана до кошика")
    else:
        messages.error(request, 'Помилка, книга не знайдена')
    
    return redirect(f"/catalog/book/{id}")

def remove(request, id):
    CartItem.objects.get(id = id).delete()

    return JsonResponse({"success": True})