from sqlalchemy.orm import Session
from sqlalchemy import or_
from api.models.Song import Song
from api.models.Artist import Artist
from api.models.ArtistGenre import ArtistGenre
from api.tools.DataTypes import Genre

from typing import List


class SongRepository:
    def get_all_songs(self, db: Session, genre_name: str) -> List[Song]:
        return (
            db.query(Song)
            .filter(
                or_(genre_name == Genre.GENERAL.name, Song.genre_name == genre_name)
            )
            .all()
        )

    def get_songs_ordered_by_date(
        self, db: Session, genre_name: str, offset: int, limit: int
    ) -> List[Song]:
        return (
            db.query(Song)
            .filter(
                or_(genre_name == Genre.GENERAL.name, Song.genre_name == genre_name)
            )
            .order_by(Song.timestamp.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_song(self, db: Session, song_id: int) -> Song:
        return db.query(Song).filter(Song.id == song_id).one()

    def create_song(self, db: Session, song: Song) -> None:
        db.add(song)
        db.commit()
        db.refresh(song)

    def create_song_artists(self, db: Session, artists: List[Artist]) -> None:
        db.add_all(artists)
        db.commit()
        for artist in artists:
            db.refresh(artist)

    def create_song_artist_genres(
        self, db: Session, artist_genres: List[ArtistGenre]
    ) -> None:
        db.add_all(artist_genres)
        db.commit()
        for genre in artist_genres:
            db.refresh(genre)

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
