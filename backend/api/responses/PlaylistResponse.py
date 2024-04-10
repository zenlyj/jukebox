from pydantic import BaseModel


class AddSongToPlaylistResponse(BaseModel):
    id: int
    session: str
    song: int
    message: str = "Successfully added to playlist!"


class DeleteSongFromPlaylistResponse(BaseModel):
    message: str


class UpdateTokenCodeResponse(BaseModel):
    message: str


class GetPlaylistSizeResponse(BaseModel):
    size: int
    message: str
