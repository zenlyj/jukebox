from pydantic import BaseModel

class ArtistBase(BaseModel):
    name: str
    song_id: int

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int

    class Config:
        orm_mode = True
