from fastapi import HTTPException
from dotenv import load_dotenv
import requests
from requests.models import Response
from typing import List
import base64
import json
import os

from api.responses.SpotifyResponse import SpotifyAuthorizationResponse
from api.responses.SpotifyResponse import SearchSpotifyResponse
from api.responses.SpotifyResponse import SpotifyUserProfileResponse
from api.responses.SpotifyResponse import SpotifyArtistResponse
from api.tools.SpotifyParser import SpotifyParser

load_dotenv()
CLIENT_URL = os.getenv("CLIENT_URL")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
USER_ENDPOINT = "https://api.spotify.com/v1/me"
ARTISTS_ENDPOINT = "https://api.spotify.com/v1/artists"


class SpotifyService:
    def create_token(self, authorization_code: str) -> SpotifyAuthorizationResponse:
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
        return self.__to_spotify_authorization_response(
            access_token, refresh_token, expires_in
        )

    def refresh_token(self, refresh_token: str) -> SpotifyAuthorizationResponse:
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
        return self.__to_spotify_authorization_response(
            access_token, refresh_token, expires_in
        )

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
            error_message = json.loads(response.text)["error"]["message"]
            raise HTTPException(status_code=response.status_code, detail=error_message)
        response_data = spotify_parser.parse_spotify_search(response.text, query)
        if not response_data:
            raise HTTPException(status_code=404, detail="Track not found on Spotify")
        name, artists_data, uri, album_cover, duration, spotify_id = response_data
        artists_spotify_id = [artist_data[1] for artist_data in artists_data]
        if any(not val for val in response_data):
            raise HTTPException(
                status_code=404, detail="Some track data is unavailable"
            )
        return self.__to_search_spotify_response(
            name, artists_spotify_id, uri, album_cover, duration, spotify_id
        )

    def get_user_profile_info(self, access_token: str) -> SpotifyUserProfileResponse:
        response = requests.get(
            USER_ENDPOINT, headers=self.__user_headers(access_token)
        )
        if response.status_code != 200:
            error_message = json.loads(response.text)["error"]["message"]
            raise HTTPException(status_code=response.status_code, detail=error_message)
        response_data = json.loads(response.text)
        name, user_id = response_data["display_name"], response_data["id"]
        return self.__to_spotify_user_profile_response(name, user_id)

    def get_artists(
        self, artists_spotify_id: str, access_token: str, spotify_parser: SpotifyParser
    ) -> List[SpotifyArtistResponse]:
        response = requests.get(
            ARTISTS_ENDPOINT,
            params=self.__artist_params(artists_spotify_id),
            headers=self.__artist_headers(access_token),
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = spotify_parser.parse_spotify_artists(response.text)
        return [
            self.__to_spotify_artist_response(name, genres, id)
            for name, genres, id in response_data
        ]

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

    def __artist_params(self, ids: str) -> dict:
        return {"ids": ids}

    def __artist_headers(self, access_token: str) -> dict:
        return {"Authorization": f"Bearer {access_token}"}

    def __handle_token_error(self, response: Response) -> None:
        error_message = json.loads(response.text)["error_description"]
        raise HTTPException(status_code=response.status_code, detail=error_message)

    def __user_headers(self, access_token: str) -> dict:
        return {"Authorization": f"Bearer {access_token}"}

    def __to_spotify_authorization_response(
        self, access_token: str, refresh_token: str, expires_in: int
    ) -> SpotifyAuthorizationResponse:
        return SpotifyAuthorizationResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )

    def __to_search_spotify_response(
        self,
        name: str,
        artists_spotify_id: List[str],
        uri: str,
        album_cover: str,
        duration: int,
        spotify_id: str,
    ) -> SearchSpotifyResponse:
        return SearchSpotifyResponse(
            name=name,
            artists_spotify_id=artists_spotify_id,
            uri=uri,
            album_cover=album_cover,
            duration=duration,
            spotify_id=spotify_id,
        )

    def __to_spotify_user_profile_response(
        self, name: str, user_id: str
    ) -> SpotifyUserProfileResponse:
        return SpotifyUserProfileResponse(name=name, user_id=user_id)

    def __to_spotify_artist_response(
        self, name: str, genres: List[str], spotify_id: str
    ) -> SpotifyArtistResponse:
        return SpotifyArtistResponse(name=name, genres=genres, spotify_id=spotify_id)
