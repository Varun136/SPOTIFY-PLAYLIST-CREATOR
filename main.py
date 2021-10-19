import requests
from bs4 import BeautifulSoup

date = input("Enter the year you want to travel (YYYY-MM-DD) :")
url =f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url)
site_html = response.text

soup = BeautifulSoup(site_html,"html.parser")
song_list = [song.text for song in soup.find_all(name="span",class_="chart-element__information__song text--truncate color--primary")]
print(song_list)

with open("songs.txt","w") as file:
    for items in song_list:
        file.write(f"{items}\n")


import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="f116d615762f4bb48e5648127bcf4548",
        client_secret="c8cba0a86ec94aaba14ce344f4772817",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

