from pydantic import BaseModel
from typing import List


class SpotifyAuthorizationResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class SearchSpotifyResponse(BaseModel):
    name: str
    artist_names: List[str]
    uri: str
    album_cover: str
    duration: int
    spotify_id: str
