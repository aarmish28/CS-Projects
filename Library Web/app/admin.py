
from django.contrib import admin
from .models import Author, Genre, Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'price')
    list_filter = ('author', 'genres')
    search_fields = ('title', 'author__name')

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
