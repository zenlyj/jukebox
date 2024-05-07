from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.database import Base


class Preference(Base):
    __tablename__ = "preference"

    id = Column(Integer, primary_key=True, index=True)
    spotify_user_id = Column(String)
    artist_genre_id = Column(Integer, ForeignKey("artist_genre.id"))

    artist_genres = relationship(
        "ArtistGenre", uselist=True, back_populates="preference"
    )
