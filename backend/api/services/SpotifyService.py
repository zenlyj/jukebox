from fastapi import HTTPException
from dotenv import load_dotenv
import requests
from requests.models import Response
from typing import List
import base64
import json
import os

from api.responses.SpotifyResponse import AuthorizeSpotifyResponse
from api.responses.SpotifyResponse import ReauthorizeSpotifyResponse
from api.responses.SpotifyResponse import SearchSpotifyResponse
from api.tools.SpotifyParser import SpotifyParser

load_dotenv()
CLIENT_URL = os.getenv("CLIENT_URL")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"


class SpotifyService:
    def get_token(self, authorization_code: str) -> AuthorizeSpotifyResponse:
        response = requests.post(
            TOKEN_ENDPOINT,
            headers=self.__token_headers(),
            data=self.__get_token_data(authorization_code),
        )
        if response.status_code != 200:
            self.__handle_token_error(response)
        response_data = json.loads(response.text)
        access_token, refresh_token, expires_in = (
            response_data["access_token"],
            response_data["refresh_token"],
            response_data["expires_in"],
        )
        return self.__to_authorize_spotify_response(
            access_token, refresh_token, expires_in
        )

    def refresh_token(self, refresh_token: str) -> ReauthorizeSpotifyResponse:
        response = requests.post(
            TOKEN_ENDPOINT,
            headers=self.__token_headers(),
            data=self.__refresh_token_data(refresh_token),
        )
        if response.status_code != 200:
            self.__handle_token_error(response)
        response_data = json.loads(response.text)
        access_token, expires_in = (
            response_data["access_token"],
            response_data["expires_in"],
        )
        return self.__to_reauthorize_spotify_response(access_token, expires_in)

    def search(
        self,
        query: str,
        query_type: str,
        access_token: str,
        spotify_parser: SpotifyParser,
    ) -> SearchSpotifyResponse:
        response = requests.get(
            SEARCH_ENDPOINT,
            headers=self.__search_headers(access_token),
            params=self.__search_params(query, query_type),
        )
        if response.status_code != 200:
            errorMessage = json.loads(response.text)["error"]["message"]
            raise HTTPException(status_code=response.status_code, detail=errorMessage)
        response_data = spotify_parser.parse_spotify_search(response.text, query)
        if not response_data:
            raise HTTPException(status_code=404, detail="Track not found on Spotify")
        name, artist_names, uri, album_cover, duration, spotify_id = response_data
        if any(not val for val in response_data):
            raise HTTPException(
                status_code=404, detail="Some track data is unavailable"
            )
        return self.__to_search_spotify_response(
            name, artist_names, uri, album_cover, duration, spotify_id
        )

    def __get_token_data(self, authorization_code: str) -> dict:
        return {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": f"{CLIENT_URL}/home/discover",
        }

    def __refresh_token_data(self, refresh_token: str) -> dict:
        return {"grant_type": "refresh_token", "refresh_token": refresh_token}

    def __token_headers(self) -> dict:
        client_credentials = base64.b64encode(
            (f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}").encode("ascii")
        ).decode("utf-8")
        return {
            "Authorization": f"Basic {client_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def __search_headers(self, access_token: str) -> dict:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    def __search_params(self, query: str, query_type: str) -> dict:
        return {"q": query, "type": query_type, "limit": 5}

    def __handle_token_error(self, response: Response) -> None:
        error_message = json.loads(response.text)["error_description"]
        raise HTTPException(status_code=response.status_code, detail=error_message)

    def __to_authorize_spotify_response(
        self, access_token: str, refresh_token: str, expires_in: int
    ) -> AuthorizeSpotifyResponse:
        return AuthorizeSpotifyResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )

    def __to_reauthorize_spotify_response(
        self, access_token: str, expires_in: int
    ) -> ReauthorizeSpotifyResponse:
        return ReauthorizeSpotifyResponse(
            access_token=access_token, expires_in=expires_in
        )

    def __to_search_spotify_response(
        self,
        name: str,
        artist_names: List[str],
        uri: str,
        album_cover: str,
        duration: int,
        spotify_id: str,
    ) -> SearchSpotifyResponse:
        return SearchSpotifyResponse(
            name=name,
            artist_names=artist_names,
            uri=uri,
            album_cover=album_cover,
            duration=duration,
            spotify_id=spotify_id,
        )
