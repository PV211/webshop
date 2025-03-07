from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from catalog.models import Book  
import logging
from django.contrib.auth.decorators import login_required
from cart.models import CartItem

logger = logging.getLogger(__name__)

def index(request):
    books = Book.objects.all()[:10]  # Отримає 10 книг з бази
    return render(request, 'home/index.html', {
        'page_title': 'Головна Сторінка',
        'books': books  
    })

def contact(request):
    return render(request, 'home/contact.html', {
        'page_title': 'Контакти'
    })

def signin(request):
    context = dict()
    context['page_title'] = 'Вхід'

    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        next = request.POST.get('next')

        user = authenticate(request, username = name, password = password)

        if user:
            login(request, user)
            messages.success(request, 'Авторизація успішна!')

            if next:
                return redirect(next)

            return redirect('/')
        else:
            messages.error(request, 'Сталася помилка під час авторизації')

    return render(request, 'home/login.html', context)

def register(request):
    context = dict()
    context['page_title'] = 'Реєстрація'

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            user = User.objects.create_user(name, email, password)

            if user:
                login(request, user)
                messages.success(request, 'Обліковий запис створено!')

                return redirect('/')
            else:
                messages.error(request, 'Сталася помилка під час реєстрації')
        else:
            messages.error(request, 'паролі не збігаються')

    return render(request, 'home/register.html', context)

def signout(request):
    logout(request)
    messages.success(request, 'Вихід успішний!')

    return redirect('/')

def about(request):
    return render(request, 'home/about.html', {
        'page_title': 'Про нас'
    })

def services(request):
    return render(request, 'home/services.html', {
        'page_title': 'Послуги'
    })

@login_required
@require_POST
def xai_consultant(request):
    user_message = request.POST.get('message')
    user = request.user

    if not user_message:
        return JsonResponse({'error': 'No message provided'}, status=400)

    # Отримуємо список книг
    books_data = list(Book.objects.values('title', 'author__name', 'price', 'stock'))
    books_info = "\n".join([f"Книга: {b['title']}, Автор: {b['author__name']}, Ціна: {b['price']} грн, Наявність: {b['stock']} шт." for b in books_data if b['author__name']])

    # Перевіряємо, чи це відповідь на пропозицію додавання
    if request.session.get('proposed_book'):
        proposed_book_title = request.session.get('proposed_book')
        book = Book.objects.filter(title=proposed_book_title).first()
        if book:
            if "так" in user_message.lower():
                if book.stock > 0:
                    cart_item, created = CartItem.objects.get_or_create(
                        book=book,
                        user=user,
                        defaults={'quantity': 1}
                    )
                    if not created:
                        cart_item.quantity += 1
                        cart_item.save()
                    book.stock -= 1
                    book.save()
                    response = f"✅ Книга '{book.title}' додана до кошика! Залишок: {book.stock} шт."
                else:
                    response = f"❌ Книга '{book.title}' відсутня на складі."
            elif "ні" in user_message.lower():
                response = f"Додавання книги '{proposed_book_title}' скасовано."
            else:
                response = f"Будь ласка, відповдіть 'так' або 'ні' для '{proposed_book_title}'."
            del request.session['proposed_book']
            return JsonResponse({'response': response})

    # Запит до Grok 2
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.XAI_API_KEY}"
    }

    data = {
        "messages": [
            {"role": "system", "content": "Ви — консультант книжкового магазину. Якщо користувач запитує про книгу, надайте інформацію з даних і запропонуйте додати її до кошика з питанням 'Чи бажаєте додати цю книгу до кошика? (Відповідь: \"так\" або \"ні\")'. Використовуйте лише надані дані."},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": f"Доступні книги:\n{books_info}"}
        ],
        "model": "grok-2-latest",
        "stream": False,
        "temperature": 0
    }

    response = requests.post('https://api.x.ai/v1/chat/completions', headers=headers, json=data)
    response.raise_for_status()

    api_response = response.json()
    if 'choices' in api_response and api_response['choices']:
        consultant_response = api_response['choices'][0]['message']['content']
        # Шукаємо пропозицію додавання до кошика
        if "чи бажаєте додати цю книгу до кошика" in consultant_response.lower():
            for book in books_data:
                if book['title'].lower() in consultant_response.lower():
                    request.session['proposed_book'] = book['title']
                    break
        return JsonResponse({'response': consultant_response})
    else:
        return JsonResponse({'error': 'Неправильна відповідь API'}, status=400)