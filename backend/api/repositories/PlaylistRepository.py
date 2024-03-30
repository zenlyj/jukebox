from sqlalchemy.orm import Session

from ..schemas import Song as song_schemas
from ..schemas import Playlist as playlist_schemas
from ..models.Song import Song
from ..models.Artist import Artist
from ..models.Playlist import Playlist

def get_playlist_songs(db: Session, session: str):
    songs = db.query(Song)\
        .join(Playlist, Song.id == Playlist.song and Playlist.session == session)\
        .all()
    res = []
    for song in songs:
        artists = db.query(Artist).filter(Artist.song_id == song.id).all()
        artist_names = [artist.name for artist in artists]
        res.append(song_schemas.Song(id=song.id, name=song.name, artist_names=artist_names, uri=song.uri, album_cover=song.album_cover, duration=song.duration))
    return res

def add_song_to_playlist(db: Session, playlist: playlist_schemas.PlaylistCreate):
    playlist_song = Playlist(session=playlist.session, song=playlist.song)
    db.add(playlist_song)
    db.commit()
    db.refresh(playlist_song)
    return playlist_song

def remove_song_from_playlist(db: Session, session: str, song_id: int):
    num_deleted = db.query(Playlist)\
                    .filter(Playlist.song == song_id and Playlist.session == session)\
                    .delete()
    db.commit()
    return num_deleted

def update_access_token_on_refresh(db: Session, old_access_token: str, new_access_token: str):
    num_updated = db.query(Playlist)\
                    .filter(Playlist.session == old_access_token)\
                    .update({Playlist.session: new_access_token})
    db.commit()
    return num_updated
