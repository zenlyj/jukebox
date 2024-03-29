from sqlalchemy import Column, ForeignKey, Integer, String

from ..database import Base

class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True, index=True)
    session = Column(String)
    song = Column(Integer, ForeignKey("songs.id"))
