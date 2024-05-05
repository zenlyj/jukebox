from sqlalchemy import Column, ForeignKey, Integer, String

from api.database import Base


class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"))
    name = Column(String)
    spotify_id = Column(String)
