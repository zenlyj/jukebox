from pydantic import BaseModel
from typing import List
from api.schemas.Song import SongOut


class GetSongResponse(BaseModel):
    songs: List[SongOut]
    song_count: int


class CreateSongResponse(BaseModel):
    song: SongOut
