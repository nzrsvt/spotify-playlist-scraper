import sys
import requests
from bs4 import BeautifulSoup

def get_spotify_playlist(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        song_links = []
        song_titles = []

        song_meta_tags = soup.find_all('meta', attrs={'name': 'music:song'})

        for tag in song_meta_tags:
            song_links.append(tag['content'])

        for link in song_links:
            response_song = requests.get(link)
            if response_song.status_code == 200:
                soup_song = BeautifulSoup(response_song.text, 'html.parser')
                title_tag = soup_song.find('title')
                if title_tag:
                    song_titles.append(title_tag.text.strip())
            else:
                print("Failed to retrieve the playlist.")
                return {}

        songs_dict = {}

        for song_info in song_titles:

            parts = song_info.split(" - song and lyrics by ")

            song_name = parts[0]
            artist_info = parts[1]

            artist = artist_info.split(" | Spotify")[0]

            songs_dict[artist] = song_name
        return(songs_dict)

    else:
        print("Failed to retrieve the playlist.")
        return {}

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