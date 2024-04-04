from pydantic import BaseModel
from typing import List

class AuthorizeSpotifyResponse(BaseModel):
    access_token: str
    refresh_token: str

class ReauthorizeSpotifyResponse(BaseModel):
    access_token: str

class SearchSpotifyResponse(BaseModel):
    name: str
    artist_names: List[str]
    uri: str
    album_cover: str
    duration: int
    spotify_id: str

def to_authorize_spotify_response(access_token: str, refresh_token: str):
    return AuthorizeSpotifyResponse(access_token=access_token, refresh_token=refresh_token)

def to_reauthorize_spotify_response(access_token: str):
    return ReauthorizeSpotifyResponse(access_token=access_token)

def to_search_spotify_response(name: str, artist_names: List[str], uri: str, album_cover: str, duration: int, spotify_id: str):
    return SearchSpotifyResponse(name=name, artist_names=artist_names, uri=uri, album_cover=album_cover, duration=duration, spotify_id=spotify_id)
