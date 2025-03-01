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
        'page_title': 'Підтвердження',
        'cart_items': cart_items
    })

def add(request, id):
    quantity = request.GET.get('quantity')

    book = Book.objects.get(id = id)

    if book:
        CartItem.objects.create(
            book = book,
            user = request.user,
            quantity = quantity if quantity else 1
        )

        messages.success(request, "Книга додана до кошика")
    else:
        messages.error(request, 'Помилка, книга не знайдена')
    
    return redirect(f"/catalog/book/{id}")

def remove(request, id):
    CartItem.objects.get(id = id).delete()

    messages.success(request, 'Книга видалена з кошика')

    return redirect('/cart')

def change(request, id):
    quantity = request.GET.get('quantity')

    cart_item = CartItem.objects.get(id = id)
    cart_item.quantity = quantity if quantity else cart_item.quantity

    cart_item.save()

    return JsonResponse({"success": True})