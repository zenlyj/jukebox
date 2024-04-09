from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..schemas import Song as song_schemas
from ..schemas import Playlist as playlist_schemas
from ..models.Song import Song
from ..models.Artist import Artist
from ..models.Playlist import Playlist

from typing import List


def get_playlist_songs(
    db: Session, session: str, page_num: int, page_size: int
) -> List[song_schemas.Song]:
    offset, limit = (page_num - 1) * page_size, page_size
    songs: List[Song] = (
        db.query(Song)
        .join(Playlist, and_(Song.id == Playlist.song, Playlist.session == session))
        .offset(offset)
        .limit(limit)
        .all()
    )
    artists: List[Artist] = (
        db.query(Artist)
        .filter(Artist.song_id.in_(set(song.id for song in songs)))
        .all()
    )
    res = []
    for song in songs:
        artist_names = [artist.name for artist in artists if artist.song_id == song.id]
        res.append(
            song_schemas.Song(
                id=song.id,
                name=song.name,
                artist_names=artist_names,
                uri=song.uri,
                album_cover=song.album_cover,
                duration=song.duration,
                spotify_id=song.spotify_id,
                genre_name=song.genre_name,
            )
        )
    return res


def add_song_to_playlist(
    db: Session, playlist: playlist_schemas.PlaylistCreate
) -> playlist_schemas.Playlist:
    playlist_song = Playlist(session=playlist.session, song=playlist.song)
    db.add(playlist_song)
    db.commit()
    db.refresh(playlist_song)
    return playlist_schemas.Playlist(
        id=playlist_song.id, session=playlist_song.session, song=playlist_song.song
    )


def remove_song_from_playlist(db: Session, session: str, song_id: int) -> int:
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


def is_song_exist(db: Session, session: str, song_id: int) -> bool:
    return (
        db.query(Playlist)
        .filter(Playlist.session == session, Playlist.song == song_id)
        .count()
        > 0
    )


def get_playlist_size(db: Session, session: str) -> int:
    return db.query(Playlist).filter(Playlist.session == session).count()
