from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.database import Base


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String)
    name = Column(String)
    uri = Column(String)
    album_cover = Column(String)
    duration = Column(Integer)
    genre_name = Column(String)
    timestamp = Column(String)

    artists = relationship("Artist", uselist=True, back_populates="song")
    playlists = relationship("Playlist", uselist=True, back_populates="song")
