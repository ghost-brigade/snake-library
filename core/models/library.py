from django.db import models
from core.models.book import Book
from core.models.book_library import BookLibrary
from accounts.models import User


class Library(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    books = models.ManyToManyField(Book, through=BookLibrary)