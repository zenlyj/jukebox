import praw
import requests
from parser import Parser
import json
import os
from dotenv import load_dotenv

parser = Parser()

load_dotenv()
CLIENT_URL = os.getenv('CLIENT_URL')
SERVER_URL = os.getenv('SERVER_URL')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')

class PrawBot:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id = REDDIT_CLIENT_ID,
            client_secret = REDDIT_CLIENT_SECRET,
            user_agent = "music_recommendation_bot",
        )

    def update(self):
        sub_name = 'hiphopheads'
        res = self.__pull(sub_name)
        for song in parser.parse(sub_name, res):
            self.__push(song)        
    
    def __pull(self, subreddit):
        titles = []
        for submission in self.reddit.subreddit(subreddit).hot(limit=500):
            titles.append(submission.title)
        return titles

    def __push(self, song):
        split = song.split('-')
        if len(split) != 2: return
        title = split[1]
        artist = split[0]
        print(self.__sanitize_song_title(title))
        print(self.__sanitize_song_artist(artist))
        uri = self.__get_song_uri(title, artist)
        print(uri)
        if (uri == None): return
        payload = {
            "title" : title,
            "artist" : artist,
            "uri" : uri
        }
        res = requests.post(f"{SERVER_URL}/songs/", data=json.dumps(payload))
        print(res.text)

    def __get_song_uri(self, title, artist):
        access_token = self.__get_access_token()
        params = {
            'query': self.__sanitize_song_title(title) + ' ' + self.__sanitize_song_artist(artist),
            'query_type': 'track',
            'access_token': access_token
        }
        res = requests.get(f"{SERVER_URL}/spotify/search", params=params)
        
        if res.status_code == 200:
            return json.loads(res.text)['uri']
        else:
            errorMessage = json.loads(res.text)['detail']
            print(errorMessage)
            if errorMessage == 'The access token expired':
                f = open('spotify_token.json', 'r')
                refresh_token = json.load(f)['refresh_token']
                self.__refresh_access_token(refresh_token)
                self.__get_song_uri(title, artist)
            return None

    def __sanitize_song_title(self, title):
        title = title.lower()
        stop_words = ['official music video', 'official video', '(', ')', '[', ']', 'produced by', 'feat. ', 'ft. ', 'ft ']
        for word in stop_words:
            title = title.replace(word, '')
        return title

    def __sanitize_song_artist(self, artist):
        artist = artist.lower()
        stop_words = ['& ', 'feat. ', 'ft. ', 'ft ', 'x ', '(', ')', '[', ']']
        for word in stop_words:
            artist = artist.replace(word, '')
        return artist

    def __get_access_token(self):
        f = open('spotify_token.json', 'r')
        return json.load(f)['access_token']

    def __refresh_access_token(self, refresh_token):
        params = {
            'refresh_token': refresh_token
        }
        res = requests.get(f"{SERVER_URL}/spotify/authorize/refresh", params=params)
        if res.status_code != 200:
            raise Exception('Unable to refresh expired access token')    
        
        refreshed_token = json.loads(res.text)['access_token']
        updated = {
            "access_token": refreshed_token,
            "refresh_token": refresh_token
        }
        with open('spotify_token.json', 'w') as outfile:
            json.dump(updated, outfile)

bot = PrawBot()
bot.update()