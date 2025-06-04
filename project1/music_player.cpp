#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <random>

using namespace std;

// Song class represents individual songs
class Song {
public:
    string title;
    string artist;

    Song(const string& title, const string& artist)
        : title(title), artist(artist) {}
};

// Playlist class represents a collection of songs
class Playlist {
public:
    string name;
    vector<Song> songs;

    Playlist(const string& name) : name(name) {}

    void addSong(const Song& song) {
        songs.push_back(song);
    }
};

// MusicPlayer class manages the music player controls
class MusicPlayer {
private:
    vector<Song> songList;
    Playlist currentPlaylist;
    size_t currentIndex;
    bool isPlaying;
    bool isShuffle;

public:
    MusicPlayer() : currentPlaylist("Default Playlist"), currentIndex(0), isPlaying(false), isShuffle(false) {}

    void addSong(const Song& song) {
        songList.push_back(song);
    }

    void setPlaylist(const Playlist& playlist) {
        currentPlaylist = playlist;
        currentIndex = 0;
    }

    void play() {
        if (!currentPlaylist.songs.empty()) {
            isPlaying = true;
            cout << "Playing: " << currentPlaylist.songs[currentIndex].title
                      << " - " << currentPlaylist.songs[currentIndex].artist << endl;
        } else {
            cout << "No songs in the playlist." << endl;
        }
    }

    void pause() {
        isPlaying = false;
        cout << "Paused." << endl;
    }

    void next() {
        if (isShuffle) {
            // Shuffle the playlist
            shuffle(currentPlaylist.songs.begin(), currentPlaylist.songs.end(), mt19937(time(0)));
        }

        if (currentIndex < currentPlaylist.songs.size() - 1) {
            currentIndex++;
        } else {
            currentIndex = 0; // Wrap around to the first song
        }

        if (isPlaying) {
            play();
        }
    }

    void previous() {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = currentPlaylist.songs.size() - 1; // Wrap around to the last song
        }

        if (isPlaying) {
            play();
        }
    }

    void toggleShuffle() {
        isShuffle = !isShuffle;
        cout << (isShuffle ? "Shuffle ON." : "Shuffle OFF.") << endl;
    }

    void printPlaylist() {
        cout << "Current Playlist: " << currentPlaylist.name << endl;
        for (const auto& song : currentPlaylist.songs) {
            cout << "  " << song.title << " - " << song.artist << endl;
        }
    }
};

int main() {
    // Creating songs
    Song song1("Song 1", "Artist 1");
    Song song2("Song 2", "Artist 2");
    Song song3("Song 3", "Artist 3");

    // Creating a playlist
    Playlist playlist("My Playlist");
    playlist.addSong(song1);
    playlist.addSong(song2);
    playlist.addSong(song3);

    // Creating a music player
    MusicPlayer player;

    // Adding songs to the music player
    player.addSong(song1);
    player.addSong(song2);
    player.addSong(song3);

    // Setting the playlist in the music player
    player.setPlaylist(playlist);

    // Printing the playlist
    player.printPlaylist();

    // Controlling the music player
    player.play();
    player.pause();
    player.next();
    player.previous();
    player.toggleShuffle();

    return 0;
}
