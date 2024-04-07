from pydantic import BaseModel
from typing import List
from api.schemas.Song import Song

class GetSongResponse(BaseModel):
    id: int
    name: str
    artist_names: List[str]
    uri: str
    album_cover: str
    duration: int
    genre_name: str

def to_get_song_response(song: Song) -> GetSongResponse:
        return GetSongResponse(id=song.id, name=song.name, artist_names=song.artist_names, uri=song.uri, album_cover=song.album_cover, duration=song.duration, genre_name=song.genre_name)
