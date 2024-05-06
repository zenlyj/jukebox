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
from api.responses.PlaylistResponse import GetPlaylistSizeResponse


class PlaylistService:
    def get_playlist_songs(
        self,
        db: Session,
        playlist_repo: PlaylistRepository,
        song_service: SongService,
        spotify_user_id: str,
        page_num: int,
        page_size: int,
    ) -> GetSongResponse:
        offset, limit = (page_num - 1) * page_size, page_size
        playlist_songs = playlist_repo.get_playlist_songs(
            db, spotify_user_id, offset, limit
        )
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
                    timestamp=song.timestamp,
                )
            )
        playlist_size = playlist_repo.get_playlist_size(db, spotify_user_id)
        return song_service.to_get_song_response(playlist_song_outputs, playlist_size)

    def get_playlist_size(
        self, db: Session, playlist_repo: PlaylistRepository, spotify_user_id: str
    ) -> GetPlaylistSizeResponse:
        size = playlist_repo.get_playlist_size(db, spotify_user_id)
        return self._to_get_playlist_size_response(size)

    def add_song_to_playlist(
        self, db: Session, playlist_repo: PlaylistRepository, playlist: PlaylistCreate
    ) -> AddSongToPlaylistResponse:
        if playlist_repo.is_song_exist(db, playlist.spotify_user_id, playlist.song_id):
            raise HTTPException(
                status_code=422, detail="Song already added to playlist!"
            )
        new_playlist_song = Playlist(
            spotify_user_id=playlist.spotify_user_id, song_id=playlist.song_id
        )
        playlist_repo.add_song_to_playlist(db, new_playlist_song)
        playlist_response_input = playlist_schemas.Playlist(
            id=new_playlist_song.id,
            spotify_user_id=new_playlist_song.spotify_user_id,
            song_id=new_playlist_song.song_id,
        )
        return self._to_add_song_to_playlist_response(playlist_response_input)

    def remove_song_from_playlist(
        self,
        db: Session,
        playlist_repo: PlaylistRepository,
        spotify_user_id: str,
        song_id: int,
    ) -> DeleteSongFromPlaylistResponse:
        num_deleted = playlist_repo.remove_song_from_playlist(
            db, spotify_user_id, song_id
        )
        if num_deleted == 0:
            raise HTTPException(status_code=422, detail="Failed to delete song")
        return self._to_delete_song_from_playlist_response(song_id)

    def _to_add_song_to_playlist_response(
        self,
        playlist_song: playlist_schemas.Playlist,
    ) -> AddSongToPlaylistResponse:
        return AddSongToPlaylistResponse(
            id=playlist_song.id,
            spotify_user_id=playlist_song.spotify_user_id,
            song_id=playlist_song.song_id,
        )

    def _to_delete_song_from_playlist_response(
        self,
        song_id: int,
    ) -> DeleteSongFromPlaylistResponse:
        message = "Successfully deleted song {song_id} from playlist!".format(
            song_id=song_id
        )
        return DeleteSongFromPlaylistResponse(message=message)

    def _to_get_playlist_size_response(
        self, playlist_size: int
    ) -> GetPlaylistSizeResponse:
        message = "{playlist_size} songs in playlist"
        return GetPlaylistSizeResponse(size=playlist_size, message=message)
