from pydantic import BaseModel


class PlaylistBase(BaseModel):
    spotify_user_id: str
    song_id: int


class PlaylistCreate(PlaylistBase):
    pass


class Playlist(PlaylistBase):
    id: int

    class Config:
        orm_mode = True
