import sys
import requests
from bs4 import BeautifulSoup

def get_spotify_playlist(url):
    pass

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <urlAddress>")
        sys.exit(1)

    url = sys.argv[1]

    playlist = get_spotify_playlist(url)

    with open("playlist.txt", "w", encoding="utf-8") as file:
        for artist, song in playlist.items():
            file.write(f"{artist} - {song}\n")
    print("Playlist saved to playlist.txt")

    for idx, (artist, song) in enumerate(playlist.items(), start=1):
        print(f"{idx}. {artist} - {song}")