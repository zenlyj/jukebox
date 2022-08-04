from sqlalchemy.orm import Session

from . import models, schemas

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()

def create_song(db: Session, song: schemas.SongCreate):
    song = models.Song(title=song.title, artist=song.artist, uri=song.uri)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song

def get_playlist_songs(db: Session, authentication_code: str):
    return db.query(models.Song)\
        .join(models.Playlist, models.Song.id == models.Playlist.song and models.Playlist.authentication_code == authentication_code)\
        .all()

def add_song_to_playlist(db: Session, playlist: schemas.PlaylistCreate):
    playlist_song = models.Playlist(authentication_code=playlist.authentication_code, song=playlist.song)
    db.add(playlist_song)
    db.commit()
    db.refresh(playlist_song)
    return playlist_song

def remove_song_from_playlist(db: Session, authentication_code: str, song_id: int):
    numDeleted = db.query(models.Playlist)\
                    .filter(models.Playlist.song == song_id and models.Playlist.authentication_code == authentication_code)\
                    .delete()
    db.commit()
    return numDeleted

def update_access_token_on_refresh(db: Session, old_access_token: str, new_access_token: str):
    numUpdated = db.query(models.Playlist)\
                    .filter(models.Playlist.authentication_code == old_access_token)\
                    .update({models.Playlist.authentication_code: new_access_token})
    db.commit()
    return numUpdated