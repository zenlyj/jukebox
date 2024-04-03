from pydantic import BaseModel

class AuthorizeSpotifyResponse(BaseModel):
    access_token: str
    refresh_token: str

class ReauthorizeSpotifyResponse(BaseModel):
    access_token: str

def to_authorize_spotify_response(access_token: str, refresh_token: str):
    return AuthorizeSpotifyResponse(access_token=access_token, refresh_token=refresh_token)

def to_reauthorize_spotify_response(access_token: str):
    return ReauthorizeSpotifyResponse(access_token=access_token)
