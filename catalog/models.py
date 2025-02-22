from django.db import models

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ім'я автора")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Національність")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Назва книги")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    pages = models.PositiveIntegerField(verbose_name="Кількість сторінок")
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True, verbose_name="Обкладинка")
    description = models.TextField(blank=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")  # Додаємо поле ціни


    def __str__(self):
        return self.title