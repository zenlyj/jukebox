from pydantic import BaseModel
from typing import List
from api.schemas.Song import Song

class SongOut(BaseModel):
    id: int
    name: str
    artist_names: List[str]
    uri: str
    album_cover: str
    duration: int
    genre_name: str

class GetSongResponse(BaseModel):
    songs: List[SongOut]
    song_count: int

class CreateSongResponse(BaseModel):
    song: SongOut

def to_song_out(song: Song):
    return SongOut(
        id=song.id,
        name=song.name,
        artist_names=song.artist_names,
        uri=song.uri,
        album_cover=song.album_cover,
        duration=song.duration,
        genre_name=song.genre_name
    )

def to_get_song_response(songs: List[Song], song_count: int) -> GetSongResponse:
    return GetSongResponse(songs=[to_song_out(song) for song in songs], song_count=song_count)

def to_create_song_response(song: Song) -> CreateSongResponse:
    return CreateSongResponse(song=to_song_out(song))
