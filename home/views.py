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

def about(request):
    return render(request, 'home/about.html', {
        'page_title': 'Про нас'
    })

def services(request):
    return render(request, 'home/services.html', {
        'page_title': 'Послуги'
    })

def signin(request):
    context = dict()
    context['page_title'] = 'Вхід'

    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username = name, password = password)

        if user:
            login(request, user)
            messages.success(request, 'Авторизація успішна!')

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

def xai_consultant(request):
    try:
        user_message = request.POST.get('message')

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Перевірка, чи містить запит "чи є у вас книга"
        if "чи є у вас книга" in user_message.lower():
            parts = user_message.split("чи є у вас книга")
            if len(parts) > 1:
                book_title = parts[1].strip().strip("'\"")
                if not book_title:
                    return JsonResponse({'error': 'Не вказано назву книги після "чи є у вас книга"'}, status=400)
                
                try:
                    # Шукаємо всі книги, що містять в назві `book_title`
                    books = Book.objects.filter(title=book_title)

                    if books.exists():
                        response_message = "Знайдені книги:\n"
                        for book in books:
                            author_name = book.author.name if book.author and book.author.name else "Невідомий автор"
                            response_message += f"'{book.title}' від {author_name}. Ціна: {book.price} грн.\n"
                    else:
                        response_message = "На жаль, такої книги у нас немає. Можу запропонувати схожі книги або рекомендації."
                except Exception as e:
                    logger.error(f"Помилка під час запиту до бази даних: {str(e)}", exc_info=True)
                    return JsonResponse({'error': 'Внутрішня помилка сервера при доступі до бази даних.'}, status=500)

                return JsonResponse({'response': response_message})

        # Якщо запит не про книгу, тоді відправляємо його до XAI API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.XAI_API_KEY}"
        }
        
        books_data = list(Book.objects.select_related('author')
                   .values('title', 'author__name', 'price', 'stock', 'genre', 'description'))

        books_info = "\n".join([
            f"Книга: {b['title']}, Автор: {b['author__name']}, Жанр: {b['genre']}, "
            f"Ціна: {b['price']} грн, Наявність: {b['stock']} шт. Про:{b['description']} "
            for b in books_data if b['author__name']
        ])

        data = {
            "messages": [
                {"role": "system", "content": "You are an online consultant for a book store. Your task is to help customers find books, provide recommendations, answer questions about books, and assist with the shopping process."},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": f"Доступні книги в магазині:\n{books_info}"}
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
            return JsonResponse({'response': consultant_response})
        else:
            return JsonResponse({'error': 'Непередбачуваний формат відповіді API'}, status=500)

    except requests.RequestException as e:
        logger.error(f"Помилка запиту до XAI API: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

    except Exception as e:
        logger.error(f"Внутрішня помилка сервера: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)