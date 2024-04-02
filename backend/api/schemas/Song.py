from pydantic import BaseModel
from typing import List

class SongBase(BaseModel):
    name: str
    artist_names: List[str]
    uri: str
    album_cover: str
    duration: int
    spotify_id: str

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int

    class Config:
        orm_mode = True
