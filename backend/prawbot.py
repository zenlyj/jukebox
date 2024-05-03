import praw
import requests
from api.tools.RedditParser import RedditParser
import json
import os
from dotenv import load_dotenv
from typing import List
from api.tools.DataTypes import Genre
from api.tools.DataTypes import SubName

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
            for title, timestamp in reddit_parser.parse(
                sub_name, self.__pull(sub_name)
            ):
                self.__push(title, genre, timestamp)

    def __pull(self, subreddit: str) -> List[object]:
        return self.reddit.subreddit(subreddit).hot(limit=500)

    def __push(self, title: str, genre: Genre, timestamp) -> None:
        print(title)
        song = self.__search_song(title)
        if not song:
            return
        song["genre_name"] = genre.name
        song["timestamp"] = timestamp
        print(song)
        res = requests.post(f"{SERVER_URL}/songs/", data=json.dumps(song))
        print(res.text)

    def __search_song(self, query: str) -> dict:
        access_token = self.__get_access_token()
        params = {"query": query, "query_type": "track", "access_token": access_token}
        res = requests.get(f"{SERVER_URL}/spotify/search", params=params)

        if res.status_code == 200:
            return json.loads(res.text)
        else:
            errorMessage = json.loads(res.text)["detail"]
            print(errorMessage)
            if errorMessage == "The access token expired":
                f = open("spotify_token.json", "r")
                refresh_token = json.load(f)["refresh_token"]
                self.__refresh_access_token(access_token, refresh_token)
                self.__search_song(query)
            return None

    def __get_access_token(self) -> str:
        f = open("spotify_token.json", "r")
        return json.load(f)["access_token"]

    def __refresh_access_token(self, expired_token: str, refresh_token: str) -> None:
        params = {"expired_token": expired_token, "refresh_token": refresh_token}
        res = requests.get(f"{SERVER_URL}/spotify/authorize/refresh", params=params)
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
