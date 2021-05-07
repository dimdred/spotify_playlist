import requests
from bs4 import BeautifulSoup
import re

import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"

while True:
    date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD \n")
    valid_value = re.search(r"\d{4}-\d{2}-\d{2}", date)
    if valid_value:
        break

response = requests.get(url=f"{URL}{date}")
response.raise_for_status()
billboard_web = response.text

soap = BeautifulSoup(billboard_web, "html.parser")
titles = soap.select("span.chart-element__information__song")
song_titles = [title.getText() for title in titles]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt"
))
user_id = sp.current_user()["id"]

song_uris = []
year = date.split('-')[0]
for song in song_titles:
    results = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = results['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)