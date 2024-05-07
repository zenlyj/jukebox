from pydantic import BaseModel
from typing import List
from api.schemas.Song import SongOut


class GetSongsResponse(BaseModel):
    songs: List[SongOut]
    song_count: int


class GetSongResponse(BaseModel):
    song: SongOut


class CreateSongResponse(BaseModel):
    song: SongOut
