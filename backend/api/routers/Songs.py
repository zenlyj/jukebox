from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas import Song as song_schemas
from api.repositories import SongRepository as song_repository
from typing import List
from ..models.responses.SongResponse import GetSongResponse
from ..models.responses.SongResponse import to_get_song_response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/songs/", response_model=List[GetSongResponse])
def get_songs(db: Session = Depends(get_db)):
    return [to_get_song_response(song) for song in song_repository.get_songs(db)]

@router.post("/songs/", response_model=GetSongResponse)
def add_songs(song: song_schemas.SongCreate, db: Session = Depends(get_db)):
    if song.spotify_id in [song.spotify_id for song in song_repository.get_songs(db)]:
        raise HTTPException(status_code=422, detail="Song already created!")
    return to_get_song_response(song_repository.create_song(db, song))
