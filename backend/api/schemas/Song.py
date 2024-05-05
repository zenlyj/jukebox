from pydantic import BaseModel
from typing import List
from api.schemas.Artist import ArtistCreate


class SongBase(BaseModel):
    name: str
    uri: str
    album_cover: str
    duration: int
    spotify_id: str
    genre_name: str
    timestamp: str


class SongCreate(SongBase):
    artists: List[ArtistCreate]


class SongOut(BaseModel):
    id: int
    name: str
    artist_names: List[str]
    uri: str
    album_cover: str
    duration: int
    genre_name: str
    timestamp: str


class Song(SongBase):
    id: int

    class Config:
        orm_mode = True
