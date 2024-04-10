from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas.Playlist import PlaylistCreate
from api.repositories.PlaylistRepository import PlaylistRepository
from api.services.PlaylistService import PlaylistService
from api.services.SongService import SongService
from api.responses.SongResponse import GetSongResponse
from api.responses.PlaylistResponse import AddSongToPlaylistResponse
from api.responses.PlaylistResponse import DeleteSongFromPlaylistResponse
from api.responses.PlaylistResponse import UpdateTokenCodeResponse
from api.responses.PlaylistResponse import GetPlaylistSizeResponse

router = APIRouter()


@router.get("/playlist/{session}", response_model=GetSongResponse)
def get_playlist_songs(
    session: str,
    page_num: int,
    page_size: int,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
    song_service: SongService = Depends(SongService),
):
    return playlist_service.get_playlist_songs(
        db, playlist_repo, song_service, session, page_num, page_size
    )


@router.get("/playlist/{session}/size", response_model=GetPlaylistSizeResponse)
def get_playlist_size(
    session: str,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
):
    return playlist_service.get_playlist_size(db, playlist_repo, session)


@router.post("/playlist/", response_model=AddSongToPlaylistResponse)
def add_song_to_playlist(
    playlist: PlaylistCreate,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
):
    return playlist_service.add_song_to_playlist(db, playlist_repo, playlist)


@router.delete(
    "/playlist/{session}/{song_id}", response_model=DeleteSongFromPlaylistResponse
)
def remove_song_from_playlist(
    session: str,
    song_id: int,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
):
    return playlist_service.remove_song_from_playlist(
        db, playlist_repo, session, song_id
    )


@router.put("/playlist/", response_model=UpdateTokenCodeResponse)
def update_token_code(
    old_access_token: str,
    new_access_token: str,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
):
    return playlist_service.update_token_code(
        db, playlist_repo, old_access_token, new_access_token
    )
