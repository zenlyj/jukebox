from fastapi import APIRouter, Depends

from api.services.SpotifyService import SpotifyService
from api.tools.SpotifyParser import SpotifyParser

from api.responses.SpotifyResponse import AuthorizeSpotifyResponse
from api.responses.SpotifyResponse import ReauthorizeSpotifyResponse
from api.responses.SpotifyResponse import SearchSpotifyResponse

router = APIRouter()


@router.get("/spotify/authorize/", response_model=AuthorizeSpotifyResponse)
def authorize_spotify(
    authorization_code: str, spotify_service: SpotifyService = Depends(SpotifyService)
):
    return spotify_service.get_token(authorization_code)


@router.get("/spotify/authorize/refresh/", response_model=ReauthorizeSpotifyResponse)
def reauthorize_spotify(
    refresh_token: str, spotify_service: SpotifyService = Depends(SpotifyService)
):
    return spotify_service.refresh_token(refresh_token)


@router.get("/spotify/search/", response_model=SearchSpotifyResponse)
def search_spotify(
    query: str,
    query_type: str,
    access_token: str,
    spotify_service: SpotifyService = Depends(SpotifyService),
    spotify_parser: SpotifyParser = Depends(SpotifyParser),
):
    return spotify_service.search(query, query_type, access_token, spotify_parser)
