from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import requests
import base64
import json
import os

from ..responses.SpotifyResponse import AuthorizeSpotifyResponse
from ..responses.SpotifyResponse import to_authorize_spotify_response
from ..responses.SpotifyResponse import ReauthorizeSpotifyResponse
from ..responses.SpotifyResponse import to_reauthorize_spotify_response
from ..responses.SpotifyResponse import SearchSpotifyResponse
from ..responses.SpotifyResponse import to_search_spotify_response
from ..tools.SpotifyParser import SpotifyParser

load_dotenv()
CLIENT_URL = os.getenv("CLIENT_URL")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

spotify_parser = SpotifyParser()
router = APIRouter()


@router.get("/spotify/authorize/", response_model=AuthorizeSpotifyResponse)
def authorize_spotify(authorization_code: str):
    client_credentials = (SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET).encode(
        "ascii"
    )
    client_credentials = base64.b64encode(client_credentials)
    headers = {
        "Authorization": "Basic " + client_credentials.decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": f"{CLIENT_URL}/home/discover",
    }
    result = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data
    )
    if result.status_code != 200:
        errorMessage = json.loads(result.text)["error_description"]
        raise HTTPException(status_code=result.status_code, detail=errorMessage)

    result = json.loads(result.text)
    access_token = result["access_token"]
    refresh_token = result["refresh_token"]

    return to_authorize_spotify_response(access_token, refresh_token)


@router.get("/spotify/authorize/refresh/", response_model=ReauthorizeSpotifyResponse)
def reauthorize_spotify(refresh_token: str):
    client_credentials = (SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET).encode(
        "ascii"
    )
    client_credentials = base64.b64encode(client_credentials)
    headers = {
        "Authorization": "Basic " + client_credentials.decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    result = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data
    )
    if result.status_code != 200:
        errorMessage = json.loads(result.text)["error_description"]
        raise HTTPException(status_code=result.status_code, detail=errorMessage)

    result = json.loads(result.text)
    access_token = result["access_token"]

    return to_reauthorize_spotify_response(access_token)


@router.get("/spotify/search/", response_model=SearchSpotifyResponse)
def search_spotify(query: str, query_type: str, access_token: str):
    print(query)
    url = "https://api.spotify.com/v1/search"
    params = {"q": query, "type": query_type, "limit": 5}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }
    result = requests.get(url, headers=headers, params=params)
    if result.status_code != 200:
        errorMessage = json.loads(result.text)["error"]["message"]
        raise HTTPException(status_code=result.status_code, detail=errorMessage)
    data = spotify_parser.parse_spotify_search(result.text, query)
    if not data:
        raise HTTPException(status_code=404, detail="Track not found on Spotify")
    name, artist_names, uri, album_cover, duration, spotify_id = data
    if any(not val for val in data):
        raise HTTPException(status_code=404, detail="Some track data is unavailable")
    return to_search_spotify_response(
        name, artist_names, uri, album_cover, duration, spotify_id
    )
