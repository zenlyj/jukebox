from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.database import Base


class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True, index=True)
    spotify_user_id = Column(String)
    song_id = Column(Integer, ForeignKey("song.id"))

    song = relationship("Song", uselist=False, back_populates="playlists")
