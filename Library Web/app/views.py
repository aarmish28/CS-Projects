from django.shortcuts import render
from .models import Book, Author, Genre
from django.db.models import Q, Count, Avg
from .models import Genre




def query_examples(request):
    
    all_books = Book.objects.all()

    
    recent_books = Book.objects.filter(publication_date__gt='2023-01-01')
    author_books = Book.objects.filter(author__name='J.K. Rowling')


    filtered_books = Book.objects.filter(
        Q(author__name='J.K. Rowling') | Q(author__name='George R.R. Martin')
    )

    
    num_books = Book.objects.count()
    average_price = Book.objects.aggregate(Avg('price'))

    return render(
        request,
        'query_examples.html',
        {
            'all_books': all_books,
            'recent_books': recent_books,
            'author_books': author_books,
            'filtered_books': filtered_books,
            'num_books': num_books,
            'average_price': average_price,
        }
    )

# Create Genre instances and save them to the database
fantasy_genre = Genre(name='Fantasy')
fantasy_genre.save()

mystery_genre = Genre(name='Mystery')
mystery_genre.save()

