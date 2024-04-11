from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.services.SongService import SongService
from api.models.Playlist import Playlist
from api.schemas.Playlist import PlaylistCreate
from api.schemas import Song as song_schemas
from api.schemas import Playlist as playlist_schemas
from api.repositories.PlaylistRepository import PlaylistRepository
from api.responses.SongResponse import GetSongResponse
from api.responses.PlaylistResponse import AddSongToPlaylistResponse
from api.responses.PlaylistResponse import DeleteSongFromPlaylistResponse
from api.responses.PlaylistResponse import UpdateTokenCodeResponse
from api.responses.PlaylistResponse import GetPlaylistSizeResponse


class PlaylistService:
    def get_playlist_songs(
        self,
        db: Session,
        playlist_repo: PlaylistRepository,
        song_service: SongService,
        session: str,
        page_num: int,
        page_size: int,
    ) -> GetSongResponse:
        offset, limit = (page_num - 1) * page_size, page_size
        playlist_songs = playlist_repo.get_playlist_songs(db, session, offset, limit)
        playlist_song_artists = playlist_repo.get_playlist_song_artists(
            db, set(song.id for song in playlist_songs)
        )
        playlist_song_outputs = []
        for song in playlist_songs:
            artist_names = [
                artist.name
                for artist in playlist_song_artists
                if artist.song_id == song.id
            ]
            playlist_song_outputs.append(
                song_schemas.SongOut(
                    id=song.id,
                    name=song.name,
                    artist_names=artist_names,
                    uri=song.uri,
                    album_cover=song.album_cover,
                    duration=song.duration,
                    genre_name=song.genre_name,
                    timestamp=song.timestamp
                )
            )
        playlist_size = playlist_repo.get_playlist_size(db, session)
        return song_service.to_get_song_response(playlist_song_outputs, playlist_size)

    def get_playlist_size(
        self, db: Session, playlist_repo: PlaylistRepository, session: str
    ) -> GetPlaylistSizeResponse:
        size = playlist_repo.get_playlist_size(db, session)
        return self.__to_get_playlist_size_response(size)

    def add_song_to_playlist(
        self, db: Session, playlist_repo: PlaylistRepository, playlist: PlaylistCreate
    ) -> AddSongToPlaylistResponse:
        if playlist_repo.is_song_exist(db, playlist.session, playlist.song):
            raise HTTPException(
                status_code=422, detail="Song already added to playlist!"
            )
        new_playlist_song = Playlist(session=playlist.session, song=playlist.song)
        playlist_repo.add_song_to_playlist(db, new_playlist_song)
        playlist_response_input = playlist_schemas.Playlist(
            id=new_playlist_song.id,
            session=new_playlist_song.session,
            song=new_playlist_song.song,
        )
        return self.__to_add_song_to_playlist_response(playlist_response_input)

    def remove_song_from_playlist(
        self, db: Session, playlist_repo: PlaylistRepository, session: str, song_id: int
    ) -> DeleteSongFromPlaylistResponse:
        num_deleted = playlist_repo.remove_song_from_playlist(db, session, song_id)
        if num_deleted == 0:
            raise HTTPException(status_code=422, detail="Failed to delete song")
        return self.__to_delete_song_from_playlist_response(song_id)

    def update_token_code(
        self,
        db: Session,
        playlist_repo: PlaylistRepository,
        old_access_token: str,
        new_access_token: str,
    ) -> UpdateTokenCodeResponse:
        num_updated = playlist_repo.update_access_token_on_refresh(
            db, old_access_token, new_access_token
        )
        return self.__to_update_token_code_response(num_updated)

    def __to_add_song_to_playlist_response(
        self,
        playlist_song: playlist_schemas.Playlist,
    ) -> AddSongToPlaylistResponse:
        return AddSongToPlaylistResponse(
            id=playlist_song.id, session=playlist_song.session, song=playlist_song.song
        )

    def __to_delete_song_from_playlist_response(
        self,
        song_id: int,
    ) -> DeleteSongFromPlaylistResponse:
        message = "Successfully deleted song {song_id} from playlist!".format(
            song_id=song_id
        )
        return DeleteSongFromPlaylistResponse(message=message)

    def __to_update_token_code_response(
        self, num_updated: int
    ) -> UpdateTokenCodeResponse:
        message = "{num_updated} songs updated".format(num_updated=num_updated)
        return UpdateTokenCodeResponse(message=message)

    def __to_get_playlist_size_response(
        self, playlist_size: int
    ) -> GetPlaylistSizeResponse:
        message = "{playlist_size} songs in playlist"
        return GetPlaylistSizeResponse(size=playlist_size, message=message)
