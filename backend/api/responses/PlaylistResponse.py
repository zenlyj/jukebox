from pydantic import BaseModel
from api.schemas.Playlist import Playlist


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


def to_add_song_to_playlist_response(
    playlist_song: Playlist,
) -> AddSongToPlaylistResponse:
    return AddSongToPlaylistResponse(
        id=playlist_song.id, session=playlist_song.session, song=playlist_song.song
    )


def to_delete_song_from_playlist_response(
    song_id: int,
) -> DeleteSongFromPlaylistResponse:
    message = "Successfully deleted song {song_id} from playlist!".format(
        song_id=song_id
    )
    return DeleteSongFromPlaylistResponse(message=message)


def to_update_token_code_response(num_updated: int) -> UpdateTokenCodeResponse:
    message = "{num_updated} songs updated".format(num_updated=num_updated)
    return UpdateTokenCodeResponse(message=message)


def to_get_playlist_size_response(playlist_size: int) -> GetPlaylistSizeResponse:
    message = "{playlist_size} songs in playlist"
    return GetPlaylistSizeResponse(size=playlist_size, message=message)
