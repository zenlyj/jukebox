from sqlalchemy import Column, ForeignKey, Integer, String

from api.database import Base


class ArtistGenre(Base):
    __tablename__ = "artist_genre"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artist.id"))
    name = Column(String)
