from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from catalog.models import Book
from .models import CartItem
from django.contrib.auth.decorators import login_required

@login_required(login_url = "/login")
def index(request):
    cart_items = CartItem.objects.filter(user = request.user)

    return render(request, 'cart/index.html', {
        'page_title': 'Кошик',
        'cart_items': cart_items
    })

def checkout(request):
    cart_items = CartItem.objects.filter(user = request.user)

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
    
    return JsonResponse({"success": True})

def remove(request, id):
    CartItem.objects.get(id = id).delete()

    messages.success(request, 'Книга видалена з кошика')

    return JsonResponse({"success": True})

def change(request, id):
    quantity = request.GET.get('quantity')

    cart_item = CartItem.objects.get(id = id)
    cart_item.quantity = quantity if quantity else cart_item.quantity

    cart_item.save()

    return JsonResponse({"success": True})

def count(request):
    cart_items = CartItem.objects.filter(user = request.user)

    return JsonResponse({"success": True, 'count': len(cart_items)})