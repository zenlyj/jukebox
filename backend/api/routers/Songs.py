from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas import Song as song_schemas
from api.repositories import SongRepository as song_repository
from typing import List

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/songs/", response_model=List[song_schemas.Song])
def get_songs(db: Session = Depends(get_db)):
    return song_repository.get_songs(db)

@router.post("/songs/", response_model=song_schemas.Song)
def add_songs(song: song_schemas.SongCreate, db: Session = Depends(get_db)):
    return song_repository.create_song(db, song)
