# Generated by Django 5.1.6 on 2025-02-22 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name="Ім'я автора")),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата народження')),
                ('nationality', models.CharField(blank=True, max_length=100, verbose_name='Національність')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва книги')),
                ('genre', models.CharField(max_length=100, verbose_name='Жанр')),
                ('pages', models.PositiveIntegerField(verbose_name='Кількість сторінок')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='book_covers/', verbose_name='Обкладинка')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='catalog.author', verbose_name='Автор')),
            ],
        ),
    ]
