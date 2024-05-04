from sqlalchemy.orm import Session
from sqlalchemy import and_

from api.models.Song import Song
from api.models.Artist import Artist
from api.models.Playlist import Playlist

from typing import List
from typing import Set


class PlaylistRepository:
    def get_playlist_songs(
        self, db: Session, spotify_user_id: str, offset: int, limit: int
    ) -> List[Song]:
        return (
            db.query(Song)
            .join(
                Playlist,
                and_(
                    Song.id == Playlist.song_id,
                    Playlist.spotify_user_id == spotify_user_id,
                ),
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_playlist_song_artists(
        self, db: Session, song_ids: Set[int]
    ) -> List[Artist]:
        return db.query(Artist).filter(Artist.song_id.in_(song_ids)).all()

    def add_song_to_playlist(self, db: Session, playlist_song: Playlist) -> None:
        db.add(playlist_song)
        db.commit()
        db.refresh(playlist_song)

    def remove_song_from_playlist(
        self, db: Session, spotify_user_id: str, song_id: int
    ) -> int:
        num_deleted = (
            db.query(Playlist)
            .filter(
                Playlist.song_id == song_id, Playlist.spotify_user_id == spotify_user_id
            )
            .delete()
        )
        db.commit()
        return num_deleted

    def is_song_exist(self, db: Session, spotify_user_id: str, song_id: int) -> bool:
        return (
            db.query(Playlist)
            .filter(
                Playlist.spotify_user_id == spotify_user_id, Playlist.song_id == song_id
            )
            .count()
            > 0
        )

    def get_playlist_size(self, db: Session, spotify_user_id: str) -> int:
        return (
            db.query(Playlist)
            .filter(Playlist.spotify_user_id == spotify_user_id)
            .count()
        )
