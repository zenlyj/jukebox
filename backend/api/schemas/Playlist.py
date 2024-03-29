from pydantic import BaseModel

class PlaylistBase(BaseModel):
    session: str
    song: int

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    id: int

    class Config:
        orm_mode = True
