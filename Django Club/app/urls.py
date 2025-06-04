from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_team/', views.create_team, name='create_team'),
    path('update_team/<int:team_id>/', views.update_team, name='update_team'),
    path('delete_team/<int:team_id>/', views.delete_team, name='delete_team'),
    path('create_player/', views.create_player, name='create_player'),
    path('update_player/<int:player_id>/', views.update_player, name='update_player'),
    path('delete_player/<int:player_id>/', views.delete_player, name='delete_player'),
]
