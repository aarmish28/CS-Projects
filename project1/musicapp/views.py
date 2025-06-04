from django.shortcuts import render
from .models import Playlist, Song
from django.http import JsonResponse

def index(request):
    playlists = Playlist.objects.all()
    songs = Song.objects.all()
    return render(request, 'index.html', {'playlists': playlists, 'songs': songs})

def play_song(request):
    if request.method == 'POST':
        song_title = request.POST.get('title')
        song_artist = request.POST.get('artist')
        # Fetch the song object based on title and artist
        # For simplicity, let's assume we directly return the audio file path
        song = Song.objects.filter(title=song_title, artist=song_artist).first()
        if song:
            return JsonResponse({'audio_file': song.audio_file.url})
        else:
            return JsonResponse({'error': 'Song not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
