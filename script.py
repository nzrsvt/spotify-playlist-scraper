import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_spotify_playlist(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        song_links = []
        song_titles = []

        song_meta_tags = soup.find_all('meta', attrs={'name': 'music:song'})

        if song_meta_tags:
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

                if artist not in songs_dict:
                    songs_dict[artist] = [song_name]
                else:
                    songs_dict[artist].append(song_name)

            return(songs_dict)
        else:
            return -1

    else:
        print("Failed to retrieve the playlist.")
        return {}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <urlAddress>")
        sys.exit(1)

    url = sys.argv[1]

    parsed_url = urlparse(url)
    if all([parsed_url.scheme, parsed_url.netloc]):
        playlist = get_spotify_playlist(url)

        if playlist:
            if playlist == -1:
                print("Couldn't recognize a playlist on a web page at the passed url.")
            else:
                with open("playlist.txt", "w", encoding="utf-8") as file:
                    for artist, songs in playlist.items():
                        for song in songs:
                            file.write(f"{artist} - {song}\n")
                print("Playlist saved to playlist.txt.")

                for artist, songs in playlist.items():
                    for song in songs:
                        print(f"{artist} - {song}")
        else:
            print("Unable to save the playlist to playlist.txt:")
    else:
        print(f"The passed {url = } is not correct.")
    