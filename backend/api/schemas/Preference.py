from pydantic import BaseModel
from typing import List


class PreferenceBase(BaseModel):
    spotify_user_id: str


class PreferenceCreate(PreferenceBase):
    song_id: int


class Preference(PreferenceBase):
    id: int
    artist_genre_id: str

    class Config:
        orm_mode = True
