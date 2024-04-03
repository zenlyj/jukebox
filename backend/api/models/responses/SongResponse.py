from pydantic import BaseModel
from typing import List
from api.schemas import Song as song_schemas

class GetSongResponse(BaseModel):
    id: int
    name: str
    artist_names: List[str]
    uri: str
    album_cover: str
    duration: int

def to_get_song_response(song: song_schemas.Song) -> GetSongResponse:
        return GetSongResponse(id=song.id, name=song.name, artist_names=song.artist_names, uri=song.uri, album_cover=song.album_cover, duration=song.duration)
