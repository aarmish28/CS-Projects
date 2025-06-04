from django.db import models

    

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=50)
    teams = models.ManyToManyField('Team')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    foundation_year = models.PositiveIntegerField()
    home_stadium = models.CharField(max_length=100)
    players = models.ManyToManyField(Player, blank=True)

    def __str__(self):
        return self.name
