from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Union
from typing_extensions import Annotated

from api.database import get_db
from api.services.SpotifyService import SpotifyService
from api.services.PlaylistService import PlaylistService
from api.repositories.PlaylistRepository import PlaylistRepository
from api.tools.SpotifyParser import SpotifyParser

from api.responses.SpotifyResponse import SpotifyAuthorizationResponse
from api.responses.SpotifyResponse import SearchSpotifyResponse
from api.responses.SpotifyResponse import SpotifyUserProfileResponse

from api.schemas.Authorization import AuthorizationCreate
from api.schemas.Authorization import AuthorizationRefresh

router = APIRouter()


@router.post("/spotify/authorization/", response_model=SpotifyAuthorizationResponse)
def authorize_spotify(
    data: Union[AuthorizationCreate, AuthorizationRefresh],
    spotify_service: SpotifyService = Depends(SpotifyService),
    playlist_service: PlaylistService = Depends(PlaylistService),
    db: Session = Depends(get_db),
    playlist_repo: PlaylistRepository = Depends(PlaylistRepository),
):
    if data.grant_type == "authorization_code":
        return spotify_service.create_token(data.authorization_code)
    elif data.grant_type == "refresh_token":
        res = spotify_service.refresh_token(data.refresh_token)
        playlist_service.update_session_id(
            db, playlist_repo, data.access_token, res.access_token
        )
        return res
    else:
        raise HTTPException(status_code=400, detail="Invalid grant type")


@router.get("/spotify/track/", response_model=SearchSpotifyResponse)
def search_spotify(
    query: str,
    query_type: str,
    access_token: str,
    spotify_service: SpotifyService = Depends(SpotifyService),
    spotify_parser: SpotifyParser = Depends(SpotifyParser),
):
    return spotify_service.search(query, query_type, access_token, spotify_parser)


@router.get("/spotify/user-profile/", response_model=SpotifyUserProfileResponse)
def get_user_profile(
    Authorization: Annotated[Union[str, None], Header()],
    spotify_service: SpotifyService = Depends(SpotifyService),
):
    return spotify_service.get_user_profile_info(Authorization)
