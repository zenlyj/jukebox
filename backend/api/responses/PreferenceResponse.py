from pydantic import BaseModel
from typing import List


class AddUserPreferencesResponse(BaseModel):
    spotify_user_id: str
    artist_genre_ids: List[int]
    message: str = "Successfully added user preferences!"


class GetUserPreferencesResponse(BaseModel):
    spotify_user_id: str
    artist_genre_ids: List[int]
