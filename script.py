import sys
import aiohttp
import aiofiles
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse

async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            print(f"Failed to retrieve the URL: {url}")
            return None

async def fetch_song_titles(session, song_links):
    song_titles = []
    for link in song_links:
        html = await fetch(session, link)
        if html:
            soup_song = BeautifulSoup(html, 'html.parser')
            title_tag = soup_song.find('title')
            if title_tag:
                song_titles.append(title_tag.text.strip())
    return song_titles

async def save_playlist_to_file(playlist, filename):
    async with aiofiles.open(filename, 'w', encoding='utf-8') as file:
        for artist, songs in playlist.items():
            for song in songs:
                await file.write(f"{artist} - {song}\n")

async def get_spotify_playlist(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            song_meta_tags = soup.find_all('meta', attrs={'name': 'music:song'})
            
            if song_meta_tags:
                song_links = [tag['content'] for tag in song_meta_tags]
                song_titles = await fetch_song_titles(session, song_links)
                
                songs_dict = {}
                for song_info in song_titles:
                    parts = song_info.split(" - song and lyrics by ")
                    if len(parts) < 2:
                        continue
                    song_name = parts[0]
                    artist_info = parts[1]
                    artist = artist_info.split(" | Spotify")[0]
                    
                    if artist not in songs_dict:
                        songs_dict[artist] = [song_name]
                    else:
                        songs_dict[artist].append(song_name)
                return songs_dict
            else:
                return -1
        else:
            return {}

async def main(url):
    parsed_url = urlparse(url)
    if all([parsed_url.scheme, parsed_url.netloc]):
        playlist = await get_spotify_playlist(url)

        if playlist:
            if playlist == -1:
                print("Couldn't recognize a playlist on a web page at the passed url.")
            else:
                await save_playlist_to_file(playlist, "playlist.txt")
                print("Playlist saved to playlist.txt:")

                for artist, songs in playlist.items():
                    for song in songs:
                        print(f"{artist} - {song}")
        else:
            print("Unable to save the playlist to playlist.txt.")
    else:
        print(f"The passed {url = } is not correct.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <urlAddress>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))