from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from catalog.models import Book  

def index(request):
    return render(request, 'home/index.html', {
        'page_title': 'Головна Сторінка'
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
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username = name, email = email, password = password)

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



@require_POST
def xai_consultant(request):
    try:
        user_message = request.POST.get('message')
        
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Логіка пошуку книги в базі даних
        if "чи є у вас книга" in user_message.lower():
            # Видаляємо зайві пробіли та лапки з назви книги
            book_title = user_message.split("чи є у вас книга")[1].strip().strip("'\"")
            
            # Пошук книги в базі даних (з урахуванням нечіткого пошуку)
            book = Book.objects.filter(title__icontains=book_title).first()
            
            if book:
                response_message = (
                    f"Так, у нас є книга '{book.title}' від {book.author.name}. "
                    f"Ціна: {book.price} грн. Наявність: {book.stock} шт."
                )
            else:
                response_message = (
                    "На жаль, такої книги у нас немає. "
                    "Можу запропонувати схожі книги або рекомендації."
                )
            
            return JsonResponse({'response': response_message})

        # Якщо запит не стосується пошуку книги, використовуємо API xAI
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.XAI_API_KEY}"
        }

        data = {
            "messages": [
                {"role": "system", "content": "You are an online consultant for a book store. Your task is to help customers find books, provide recommendations, answer questions about books, and assist with the shopping process."},
                {"role": "user", "content": user_message}
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
            return JsonResponse({'error': 'Unexpected API response format'}, status=500)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)
    


def xai_consultant(request):
    try:
        user_message = request.POST.get('message')
        
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.XAI_API_KEY}"
        }

        data = {
            "messages": [
                {"role": "system", "content": "You are an online consultant for a book store. Your task is to help customers find books, provide recommendations, answer questions about books, and assist with the shopping process."},
                {"role": "user", "content": user_message}
            ],
            "model": "grok-2-latest",
            "stream": False,
            "temperature": 0
        }

        response = requests.post('https://api.x.ai/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        
        # Додаткова логіка для обробки відповіді, наприклад, форматування чи вилучення певної інформації
        api_response = response.json()
        if 'choices' in api_response and api_response['choices']:
            consultant_response = api_response['choices'][0]['message']['content']
            return JsonResponse({'response': consultant_response})
        else:
            return JsonResponse({'error': 'Unexpected API response format'}, status=500)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

# ШІ для пошуку книг на майбутнє зразок
# @require_POST
# def xai_consultant(request):
    try:
        user_message = request.POST.get('message')
        
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.XAI_API_KEY}"
        }

        # Перевірка на наявність книги в базі даних
        if "чи є у вас книга" in user_message.lower():
            book_title = user_message.split("чи є у вас книга")[1].strip().strip("'\"")
            book = Book.objects.filter(title__icontains=book_title).first()
            if book:
                response_message = f"Так, у нас є книга '{book.title}' від {book.author}. Ціна: {book.price} грн. Наявність: {book.stock} шт."
            else:
                response_message = "На жаль, такої книги у нас немає. Можу запропонувати схожі книги або рекомендації."
            
            return JsonResponse({'response': response_message})

        data = {
            "messages": [
                {"role": "system", "content": "You are an online consultant for a book store. Your task is to help customers find books, provide recommendations, answer questions about books, and assist with the shopping process."},
                {"role": "user", "content": user_message}
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
            return JsonResponse({'error': 'Unexpected API response format'}, status=500)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


def consult_page(request):
    return render(request, 'consult.html')