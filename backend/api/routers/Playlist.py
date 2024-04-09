from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas.Playlist import PlaylistCreate
from api.repositories import PlaylistRepository as playlist_repository
from typing import List
from ..responses.SongResponse import GetSongResponse
from ..responses.SongResponse import to_get_song_response
from ..responses.PlaylistResponse import AddSongToPlaylistResponse
from ..responses.PlaylistResponse import to_add_song_to_playlist_response
from ..responses.PlaylistResponse import DeleteSongFromPlaylistResponse
from ..responses.PlaylistResponse import to_delete_song_from_playlist_response
from ..responses.PlaylistResponse import UpdateTokenCodeResponse
from ..responses.PlaylistResponse import to_update_token_code_response

router = APIRouter()


@router.get("/playlist/{session}", response_model=List[GetSongResponse])
def get_playlist_songs(session: str, db: Session = Depends(get_db)):
    return [
        to_get_song_response(song)
        for song in playlist_repository.get_playlist_songs(db, session)
    ]


@router.post("/playlist/", response_model=AddSongToPlaylistResponse)
def add_song_to_playlist(playlist: PlaylistCreate, db: Session = Depends(get_db)):
    if playlist_repository.is_song_exist(db, playlist.session, playlist.song):
        raise HTTPException(status_code=422, detail="Song already added to playlist!")
    return to_add_song_to_playlist_response(
        playlist_repository.add_song_to_playlist(db, playlist)
    )


@router.delete("/playlist/", response_model=DeleteSongFromPlaylistResponse)
def remove_song_from_playlist(
    session: str, song_id: int, db: Session = Depends(get_db)
):
    numDeleted = playlist_repository.remove_song_from_playlist(db, session, song_id)
    if numDeleted == 0:
        raise HTTPException(status_code=422, detail="Failed to delete song")
    return to_delete_song_from_playlist_response(song_id)


@router.put("/playlist/", response_model=UpdateTokenCodeResponse)
def update_token_code(
    old_access_token: str, new_access_token: str, db: Session = Depends(get_db)
):
    numUpdated = playlist_repository.update_access_token_on_refresh(
        db, old_access_token, new_access_token
    )
    return to_update_token_code_response(numUpdated)
