# Spotify Playlist Scraper
## Overview
This Python script allows you to extract a list of songs from a Spotify playlist URL. It retrieves song information including the artist and song name from the provided playlist URL and saves it to a text file.

## Usage
To use this script, you'll need Python installed on your system. Follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies listed in requirements.txt using pip install -r requirements.txt.
3. Run the script by executing the following command in your terminal or command prompt:
```bash
python script.py <urlAddress>
```
> [!NOTE]
> Replace ```<urlAddress>``` with the URL of the Spotify playlist you want to scrape.

## Requirements
The script requires the following Python modules, which are listed in the **'requirements.txt'** file:

* BeautifulSoup4
* Certifi
* Charset-normalizer
* Idna
* Requests
* Soupsieve
* Urllib3

## Output
After running the script with the specified Spotify playlist URL, a file named playlist.txt will be created in the same directory. This file will contain a list of songs extracted from the playlist, with each entry formatted as follows:
```bash
<Artist> - <Song>
```
Additionally, the script will display the extracted playlist on the console, listing each song with its corresponding artist.

> [!WARNING]
> Please make sure you have the necessary permissions to access the Spotify playlist URL. Additionally, ensure that the playlist is publicly accessible, as private playlists may not be scraped successfully.

---
Feel free to contribute to this project or report any issues on GitHub.