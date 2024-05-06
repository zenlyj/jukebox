import praw
import requests
from api.tools.RedditParser import RedditParser
import json
import os
from dotenv import load_dotenv
from typing import List
from api.tools.DataTypes import Genre
from api.tools.DataTypes import SubName
from api.schemas.Artist import ArtistCreate
from api.schemas.Song import SongCreate

reddit_parser = RedditParser()

load_dotenv()
CLIENT_URL = os.getenv("CLIENT_URL")
SERVER_URL = os.getenv("SERVER_URL")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")


class PrawBot:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="music_recommendation_bot",
        )

    def update(self) -> None:
        for genre in [Genre.HIPHOP, Genre.ELECTRONIC, Genre.INDIE]:
            sub_name = SubName[genre]
            for title, timestamp in reddit_parser.parse(sub_name, self._pull(sub_name)):
                self._push(title, genre, timestamp)

    def _pull(self, subreddit: str) -> List[object]:
        return self.reddit.subreddit(subreddit).hot(limit=500)

    def _push(self, title: str, genre: Genre, timestamp) -> None:
        print(title)
        song = self._search_song(title)
        if not song:
            return
        song["genre_name"] = genre.name
        song["timestamp"] = timestamp
        artists = self._get_artists(song["artists_spotify_id"])
        song_artists_payload = [
            ArtistCreate(
                name=artist["name"],
                genres=artist["genres"],
                spotify_id=artist["spotify_id"],
            )
            for artist in artists
        ]
        song_payload = SongCreate(
            name=song["name"],
            uri=song["uri"],
            album_cover=song["album_cover"],
            duration=song["duration"],
            spotify_id=song["spotify_id"],
            genre_name=song["genre_name"],
            timestamp=song["timestamp"],
            artists=song_artists_payload,
        )
        res = requests.post(
            f"{SERVER_URL}/songs/", data=song_payload.model_dump_json().encode("utf-8")
        )
        print(res.text)

    def _get_artists(self, spotify_ids: List[str]) -> dict:
        access_token = self._get_access_token()
        params = {"ids": ",".join(spotify_ids)}
        headers = {"Authorization": f"Bearer {access_token}"}
        res = requests.get(
            f"{SERVER_URL}/spotify/artists/", params=params, headers=headers
        )
        if res.status_code != 200:
            print(res.text)
            raise Exception("Unable to get artists")
        return json.loads(res.text)

    def _search_song(self, query: str) -> dict:
        access_token = self._get_access_token()
        params = {"query": query, "query_type": "track"}
        headers = {"Authorization": f"Bearer {access_token}"}
        res = requests.get(
            f"{SERVER_URL}/spotify/track", params=params, headers=headers
        )

        if res.status_code == 200:
            return json.loads(res.text)
        else:
            errorMessage = json.loads(res.text)["detail"]
            print(errorMessage)
            if errorMessage == "The access token expired":
                f = open("spotify_token.json", "r")
                refresh_token = json.load(f)["refresh_token"]
                self._refresh_access_token(access_token, refresh_token)
                self._search_song(query)
            return None

    def _get_access_token(self) -> str:
        f = open("spotify_token.json", "r")
        return json.load(f)["access_token"]

    def _refresh_access_token(self, expired_token: str, refresh_token: str) -> None:
        auth_data = {
            "grant_type": "refresh_token",
            "authorization_code": None,
            "access_token": expired_token,
            "refresh_token": refresh_token,
        }
        res = requests.post(
            f"{SERVER_URL}/spotify/authorization/", data=json.dumps(auth_data)
        )
        if res.status_code != 200:
            raise Exception("Unable to refresh expired access token")

        response_data = json.loads(res.text)
        updated = {
            "access_token": response_data["access_token"],
            "refresh_token": refresh_token,
            "expires_in": response_data["expires_in"],
        }
        with open("spotify_token.json", "w") as outfile:
            json.dump(updated, outfile)


bot = PrawBot()
bot.update()
