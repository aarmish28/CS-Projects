from django.db import models

class Crud(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    address = models.TextField()
    phone = models.IntegerField()

    def __str__(self):
        return self.name
    
