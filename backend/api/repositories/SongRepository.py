from sqlalchemy.orm import Session
from sqlalchemy import or_
from api.models.Song import Song
from api.models.Artist import Artist
from api.tools.DataTypes import Genre

from typing import List
from typing import Set


class SongRepository:
    def get_songs(
        self, db: Session, genre_name: str, offset: int, limit: int
    ) -> List[Song]:
        return (
            db.query(Song)
            .filter(
                or_(genre_name == Genre.GENERAL.name, Song.genre_name == genre_name)
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_song_artists(self, db: Session, song_ids: Set[int]) -> List[Artist]:
        return db.query(Artist).filter(Artist.song_id.in_(song_ids)).all()

    def create_song(self, db: Session, song: Song) -> None:
        db.add(song)
        db.commit()
        db.refresh(song)

    def create_song_artists(self, db: Session, artists: List[Artist]) -> None:
        db.add_all(artists)
        db.commit()
        for artist in artists:
            db.refresh(artist)

    def is_song_exist(self, db: Session, spotify_id: str) -> bool:
        return db.query(Song).filter(Song.spotify_id == spotify_id).count() > 0

    def get_song_count(self, db: Session, genre_name: str) -> int:
        return (
            db.query(Song)
            .filter(
                or_(genre_name == Genre.GENERAL.name, Song.genre_name == genre_name)
            )
            .count()
        )
