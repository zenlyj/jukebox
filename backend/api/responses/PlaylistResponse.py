from pydantic import BaseModel


class AddSongToPlaylistResponse(BaseModel):
    id: int
    spotify_user_id: str
    song_id: int
    message: str = "Successfully added to playlist!"


class DeleteSongFromPlaylistResponse(BaseModel):
    message: str


class GetPlaylistSizeResponse(BaseModel):
    size: int
    message: str
