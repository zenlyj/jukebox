from typing import List, Union

from pydantic import BaseModel

class SongBase(BaseModel):
    title: str
    artist: str
    uri: str

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int

    class Config:
        orm_mode = True

class PlaylistBase(BaseModel):
    session: str
    song: int

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    id: int

    class Config:
        orm_mode = True