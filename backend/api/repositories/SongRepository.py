from sqlalchemy.orm import Session

from ..schemas import Song as song_schemas
from ..models.Song import Song

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Song).offset(skip).limit(limit).all()

def create_song(db: Session, song: song_schemas.SongCreate):
    song = Song(title=song.title, artist=song.artist, uri=song.uri)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song
