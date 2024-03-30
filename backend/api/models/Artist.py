from sqlalchemy import Column, ForeignKey, Integer, String

from ..database import Base

class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    song_id = Column(Integer, ForeignKey("songs.id"))
