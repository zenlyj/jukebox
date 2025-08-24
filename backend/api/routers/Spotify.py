from fastapi import APIRouter, Depends, Header
from typing import Union, List
from typing_extensions import Annotated

from api.services import SpotifyService
from api.tools.SpotifyParser import SpotifyParser

from api.responses.SpotifyResponse import SpotifyAuthorizationResponse
from api.responses.SpotifyResponse import SearchSpotifyResponse
from api.responses.SpotifyResponse import SpotifyUserProfileResponse
from api.responses.SpotifyResponse import SpotifyArtistResponse

from api.schemas.Authorization import AuthorizationCreate
from api.schemas.Authorization import AuthorizationRefresh

from api.exceptions.DomainException import DomainException

router = APIRouter()


@router.post("/spotify/authorization/", response_model=SpotifyAuthorizationResponse)
def authorize_spotify(
    data: Union[AuthorizationCreate, AuthorizationRefresh],
    spotify_service: SpotifyService = Depends(SpotifyService),
):
    if data.grant_type == "authorization_code":
        return spotify_service.create_token(data.authorization_code)
    elif data.grant_type == "refresh_token":
        return spotify_service.refresh_token(data.refresh_token)
    else:
        raise DomainException(status_code=400, detail="Invalid grant type")


@router.get("/spotify/track/", response_model=SearchSpotifyResponse)
def search_spotify(
    query: str,
    query_type: str,
    Authorization: Annotated[Union[str, None], Header()],
    spotify_service: SpotifyService = Depends(SpotifyService),
    spotify_parser: SpotifyParser = Depends(SpotifyParser),
):
    _, access_token = Authorization.split()
    return spotify_service.search(query, query_type, access_token, spotify_parser)


@router.get("/spotify/user-profile/", response_model=SpotifyUserProfileResponse)
def get_user_profile(
    Authorization: Annotated[Union[str, None], Header()],
    spotify_service: SpotifyService = Depends(SpotifyService),
):
    _, access_token = Authorization.split()
    return spotify_service.get_user_profile_info(access_token)


@router.get("/spotify/artists/", response_model=List[SpotifyArtistResponse])
def get_artists(
    ids: str,
    Authorization: Annotated[Union[str, None], Header()],
    spotify_service: SpotifyService = Depends(SpotifyService),
    spotify_parser: SpotifyParser = Depends(SpotifyParser),
):
    _, access_token = Authorization.split()
    return spotify_service.get_artists(ids, access_token, spotify_parser)
