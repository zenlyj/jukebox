from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.database import Base


class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String)
    song_id = Column(Integer, ForeignKey("song.id"))
    name = Column(String)

    artist_genres = relationship("ArtistGenre", uselist=True, back_populates="artist")
    song = relationship("Song", uselist=False, back_populates="artists")
