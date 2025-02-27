from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Book, Author, Genre
from django.contrib import messages
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render




@staff_member_required
def product_dashboard(request):
    return render(request, 'product_admin/dashboard.html')

def product_list(request):
    books = Book.objects.all()
    return render(request, 'product_admin/product_list.html', {'books': books})

def product_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.price = request.POST.get('price')
        book.stock = request.POST.get('stock')
        book.save()
        messages.success(request, 'Книга оновлена!')
        return redirect('product_list')

    return render(request, 'product_admin/product_edit.html', {'book': book})

def product_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Книга видалена!')
    return redirect('product_list')

def product_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        genre_id = request.POST.get('genre')
        pages = request.POST.get('pages')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        cover_image = request.FILES.get('cover_image')  # Отримання файлу

        author = get_object_or_404(Author, id=author_id)
        genre = get_object_or_404(Genre, id=genre_id)

        # Створення нового запису
        new_book = Book.objects.create(
            title=title,
            author=author,
            genre=genre,
            pages=pages,
            price=price,
            stock=stock,
            description=description,
            cover_image=cover_image  # Збереження зображення
        )

        messages.success(request, 'Книга успішно додана!')
        return redirect('product_list')

    authors = Author.objects.all()
    genres = Genre.objects.all()

    return render(request, 'product_admin/product_add.html', {'authors': authors, 'genres': genres})

def author_add(request):
    """ Додавання нового автора """
    if request.method == "POST":
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        nationality = request.POST.get('nationality')

        if name:
            Author.objects.create(name=name, birth_date=birth_date, nationality=nationality)
            messages.success(request, "Автор успішно доданий!")
            return redirect('product_dashboard')
        else:
            messages.error(request, "Помилка: потрібно вказати ім'я автора!")

    return render(request, 'product_admin/author_add.html')

def genre_add(request):
    """ Додавання нового жанру """
    if request.method == "POST":
        name = request.POST.get('name')

        if name:
            Genre.objects.create(name=name)
            messages.success(request, "Жанр успішно доданий!")
            return redirect('product_dashboard')
        else:
            messages.error(request, "Помилка: потрібно вказати назву жанру!")

    return render(request, 'product_admin/genre_add.html')