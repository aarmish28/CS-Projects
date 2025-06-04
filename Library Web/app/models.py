from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title
