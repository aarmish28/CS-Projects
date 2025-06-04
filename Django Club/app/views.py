from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Player

def home(request):
    teams = Team.objects.all()
    players = Player.objects.all()
    return render(request, 'home.html', {'teams': teams, 'players': players})

def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        foundation_year = request.POST.get('foundation_year')
        home_stadium = request.POST.get('home_stadium')
        Team.objects.create(name=name, foundation_year=foundation_year, home_stadium=home_stadium)
        return redirect('home')
    return render(request, 'home.html')

def update_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        team.name = request.POST.get('name')
        team.foundation_year = request.POST.get('foundation_year')
        team.home_stadium = request.POST.get('home_stadium')
        team.save()
        return redirect('home')
    return render(request, 'home.html', {'team': team})

def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        team.delete()
        return redirect('home')
    return render(request, 'home.html', {'team': team})

def create_player(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        nationality = request.POST.get('nationality')
        player = Player.objects.create(first_name=first_name, last_name=last_name, birth_date=birth_date, nationality=nationality)
        teams_selected = request.POST.getlist('teams')
        for team_id in teams_selected:
            team = get_object_or_404(Team, pk=team_id)
            player.teams.add(team)
        return redirect('home')
    return render(request, 'home.html')

def update_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        player.first_name = request.POST.get('first_name')
        player.last_name = request.POST.get('last_name')
        player.birth_date = request.POST.get('birth_date')
        player.nationality = request.POST.get('nationality')
        player.save()
        player.teams.clear()
        teams_selected = request.POST.getlist('teams')
        for team_id in teams_selected:
            team = get_object_or_404(Team, pk=team_id)
            player.teams.add(team)
        return redirect('home')
    return render(request, 'home.html', {'player': player})

def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        player.delete()
        return redirect('home')
    return render(request, 'home.html', {'player': player})
