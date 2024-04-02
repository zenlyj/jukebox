from sqlalchemy.orm import Session

from ..schemas import Song as song_schemas
from ..models.Song import Song
from ..models.Artist import Artist

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    songs = db.query(Song).offset(skip).limit(limit).all()
    res = []
    for song in songs:
        artists = db.query(Artist).filter(Artist.song_id == song.id)
        artist_names = [artist.name for artist in artists]
        res.append(song_schemas.Song(id=song.id, name=song.name, artist_names=artist_names, uri=song.uri, album_cover=song.album_cover, duration=song.duration, spotify_id=song.spotify_id))
    return res

def create_song(db: Session, song: song_schemas.SongCreate):
    new_song = Song(name=song.name, uri=song.uri, album_cover=song.album_cover, duration=song.duration, spotify_id=song.spotify_id)
    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    artists = [Artist(name=artist_name, song_id=new_song.id) for artist_name in song.artist_names]
    artist_names = [artist.name for artist in artists]
    db.add_all(artists)
    db.commit()
    for artist in artists:
        db.refresh(artist)
    return song_schemas.Song(id=new_song.id, name=new_song.name, artist_names=artist_names, uri=new_song.uri, album_cover=new_song.album_cover, duration=new_song.duration, spotify_id=song.spotify_id)
