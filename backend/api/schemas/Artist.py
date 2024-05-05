from pydantic import BaseModel
from typing import List


class ArtistBase(BaseModel):
    name: str
    spotify_id: str


class ArtistCreate(ArtistBase):
    genres: List[str]


class Artist(ArtistBase):
    id: int
    song_id: int

    class Config:
        orm_mode = True
