from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.database import Base


class ArtistGenre(Base):
    __tablename__ = "artist_genre"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artist.id"))
    name = Column(String)

    artist = relationship("Artist", uselist=False, back_populates="artist_genres")
    preference = relationship(
        "Preference", uselist=False, back_populates="artist_genres"
    )
