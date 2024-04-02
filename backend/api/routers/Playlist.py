from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas import Song as song_schemas
from api.schemas import Playlist as playlist_schemas
from api.repositories import PlaylistRepository as playlist_repository
from typing import List
from ..models.SongResponse import SongResponse
from ..models.SongResponse import toResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/playlist/", response_model=List[SongResponse])
def get_playlist_songs(session: str, db: Session = Depends(get_db)):
    return [toResponse(song) for song in playlist_repository.get_playlist_songs(db, session)]

@router.post("/playlist/", response_model=playlist_schemas.Playlist)
def add_song_to_playlist(playlist: playlist_schemas.PlaylistCreate, db: Session = Depends(get_db)):
    if playlist.song in [song.id for song in playlist_repository.get_playlist_songs(db, playlist.session)]:
        raise HTTPException(status_code=422, detail="Song already added to playlist!")
    return playlist_repository.add_song_to_playlist(db, playlist)

@router.delete("/playlist/")
def remove_song_from_playlist(session: str, song_id: int, db: Session = Depends(get_db)):
    numDeleted = playlist_repository.remove_song_from_playlist(db, session, song_id)
    if numDeleted == 0:
        raise HTTPException(status_code=422, detail='Failed to delete song')
    return {
        'detail': 'Delete Successful'
    }

@router.put('/playlist/')
def update_token_code(old_access_token: str, new_access_token: str, db: Session = Depends(get_db)):
    numUpdated = playlist_repository.update_access_token_on_refresh(db, old_access_token, new_access_token)
    return {
        'detail': '{x} songs updated'.format(x=numUpdated)
    }
