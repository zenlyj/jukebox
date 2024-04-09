from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas.Song import SongCreate
from api.repositories import SongRepository as song_repository
from typing import List
from ..responses.SongResponse import GetSongResponse
from ..responses.SongResponse import to_get_song_response
from ..responses.SongResponse import CreateSongResponse
from ..responses.SongResponse import to_create_song_response


router = APIRouter()


@router.get("/songs/", response_model=GetSongResponse)
def get_songs(
    genre_name: str,
    page_num: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
):
    songs = song_repository.get_songs(db, genre_name, page_num, page_size)
    song_count = song_repository.get_song_count(db, genre_name)
    return to_get_song_response(songs, song_count)


@router.post("/songs/", response_model=CreateSongResponse)
def add_songs(song: SongCreate, db: Session = Depends(get_db)):
    if song_repository.is_song_exist(db, song.spotify_id):
        raise HTTPException(status_code=422, detail="Song already created!")
    return to_create_song_response(song_repository.create_song(db, song))
