from pydantic import BaseModel
from typing import List


class ArtistGenreBase(BaseModel):
    artist_id: str
    name: str


class ArtistGenreCreate(ArtistGenreBase):
    pass


class ArtistGenre(ArtistGenreBase):
    id: int

    class Config:
        orm_mode = True
