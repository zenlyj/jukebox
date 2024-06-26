from pydantic import BaseModel
from typing import List


class SpotifyAuthorizationResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class SearchSpotifyResponse(BaseModel):
    name: str
    artists_spotify_id: List[str]
    uri: str
    album_cover: str
    duration: int
    spotify_id: str


class SpotifyUserProfileResponse(BaseModel):
    name: str
    user_id: str


class SpotifyArtistResponse(BaseModel):
    name: str
    genres: List[str]
    spotify_id: str
