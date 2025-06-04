from django.contrib import admin
from .models import Team, Player

admin.site.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'foundation_year', 'home_stadium')

admin.site.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date', 'nationality')
    filter_horizontal = ('teams',)
