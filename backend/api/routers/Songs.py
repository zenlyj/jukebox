from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas.Song import SongCreate
from api.repositories.SongRepository import SongRepository
from api.services.SongService import SongService
from api.responses.SongResponse import GetSongsResponse
from api.responses.SongResponse import CreateSongResponse


router = APIRouter()


@router.get("/songs/", response_model=GetSongsResponse)
def get_songs(
    genre_name: str,
    page_num: int,
    page_size: int,
    db: Session = Depends(get_db),
    song_repo: SongRepository = Depends(SongRepository),
    song_service: SongService = Depends(SongService),
):
    return song_service.get_songs(db, song_repo, genre_name, page_num, page_size)


@router.post("/songs/", response_model=CreateSongResponse)
def add_songs(
    song: SongCreate,
    db: Session = Depends(get_db),
    song_repo: SongRepository = Depends(SongRepository),
    song_service: SongService = Depends(SongService),
):
    return song_service.add_song(db, song_repo, song)
