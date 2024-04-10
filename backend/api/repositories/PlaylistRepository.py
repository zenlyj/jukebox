from sqlalchemy.orm import Session
from sqlalchemy import and_

from api.models.Song import Song
from api.models.Artist import Artist
from api.models.Playlist import Playlist

from typing import List
from typing import Set


class PlaylistRepository:
    def get_playlist_songs(
        self, db: Session, session: str, offset: int, limit: int
    ) -> List[Song]:
        return (
            db.query(Song)
            .join(Playlist, and_(Song.id == Playlist.song, Playlist.session == session))
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

    def remove_song_from_playlist(self, db: Session, session: str, song_id: int) -> int:
        num_deleted = (
            db.query(Playlist)
            .filter(Playlist.song == song_id, Playlist.session == session)
            .delete()
        )
        db.commit()
        return num_deleted

    def update_access_token_on_refresh(
        db: Session, old_access_token: str, new_access_token: str
    ) -> int:
        num_updated = (
            db.query(Playlist)
            .filter(Playlist.session == old_access_token)
            .update({Playlist.session: new_access_token})
        )
        db.commit()
        return num_updated

    def is_song_exist(self, db: Session, session: str, song_id: int) -> bool:
        return (
            db.query(Playlist)
            .filter(Playlist.session == session, Playlist.song == song_id)
            .count()
            > 0
        )

    def get_playlist_size(self, db: Session, session: str) -> int:
        return db.query(Playlist).filter(Playlist.session == session).count()
