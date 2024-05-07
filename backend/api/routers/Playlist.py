from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas.Playlist import PlaylistCreate
from api.repositories.PlaylistRepository import PlaylistRepository
from api.services.PlaylistService import PlaylistService
from api.services.SongService import SongService
from api.responses.SongResponse import GetSongsResponse
from api.responses.PlaylistResponse import AddSongToPlaylistResponse
from api.responses.PlaylistResponse import DeleteSongFromPlaylistResponse
from api.responses.PlaylistResponse import GetPlaylistSizeResponse

router = APIRouter()


@router.get("/playlist/", response_model=GetSongsResponse)
def get_playlist_songs(
    spotify_user_id: str,
    page_num: int,
    page_size: int,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
    song_service: SongService = Depends(SongService),
):
    return playlist_service.get_playlist_songs(
        db, playlist_repo, song_service, spotify_user_id, page_num, page_size
    )


@router.get("/playlist/size/", response_model=GetPlaylistSizeResponse)
def get_playlist_size(
    spotify_user_id: str,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
):
    return playlist_service.get_playlist_size(db, playlist_repo, spotify_user_id)


@router.post("/playlist/", response_model=AddSongToPlaylistResponse)
def add_song_to_playlist(
    playlist: PlaylistCreate,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
):
    return playlist_service.add_song_to_playlist(db, playlist_repo, playlist)


@router.delete("/playlist/", response_model=DeleteSongFromPlaylistResponse)
def remove_song_from_playlist(
    spotify_user_id: str,
    song_id: int,
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
    playlist_service: PlaylistService = Depends(PlaylistService),
):
    return playlist_service.remove_song_from_playlist(
        db, playlist_repo, spotify_user_id, song_id
    )
