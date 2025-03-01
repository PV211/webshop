from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book

class CartItem(models.Model):
    book = models.ForeignKey(Book, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return str(self.book.title)