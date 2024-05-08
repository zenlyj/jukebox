from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.repositories.SongRepository import SongRepository
from api.responses.SongResponse import GetSongsResponse
from api.responses.SongResponse import CreateSongResponse
from api.schemas import Song as song_schemas
from api.models.Song import Song
from api.models.Artist import Artist
from api.models.ArtistGenre import ArtistGenre


class SongService:
    def get_songs(
        self,
        db: Session,
        song_repo: SongRepository,
        genre_name: str,
        page_num: int,
        page_size: int,
    ) -> GetSongsResponse:
        offset, limit = (page_num - 1) * page_size, page_size
        songs = song_repo.get_songs(db, genre_name, offset, limit)
        song_outputs = [
            song_schemas.SongOut(
                id=song.id,
                name=song.name,
                artist_names=[artist.name for artist in song.artists],
                uri=song.uri,
                album_cover=song.album_cover,
                duration=song.duration,
                genre_name=song.genre_name,
                timestamp=song.timestamp,
            )
            for song in songs
        ]
        song_count = song_repo.get_song_count(db, genre_name)
        return self.to_get_songs_response(song_outputs, song_count)

    def add_song(
        self, db: Session, song_repo: SongRepository, song: song_schemas.SongCreate
    ) -> CreateSongResponse:
        if song_repo.is_song_exist(db, song.spotify_id):
            raise HTTPException(status_code=422, detail="Song already created!")
        new_song = Song(
            name=song.name,
            uri=song.uri,
            album_cover=song.album_cover,
            duration=song.duration,
            spotify_id=song.spotify_id,
            genre_name=song.genre_name,
            timestamp=song.timestamp,
        )
        song_repo.create_song(db, new_song)

        new_song_artists = []
        for artist in song.artists:
            new_song_artist = Artist(
                name=artist.name, song_id=new_song.id, spotify_id=artist.spotify_id
            )
            song_repo.create_song_artists(db, [new_song_artist])
            song_repo.create_song_artist_genres(
                db,
                [
                    ArtistGenre(artist_id=new_song_artist.id, name=genre)
                    for genre in artist.genres
                ],
            )
            new_song_artists.append(new_song_artist)
        song_output = song_schemas.SongOut(
            id=new_song.id,
            name=new_song.name,
            artist_names=[artist.name for artist in new_song_artists],
            uri=new_song.uri,
            album_cover=new_song.album_cover,
            duration=new_song.duration,
            genre_name=new_song.genre_name,
            timestamp=new_song.timestamp,
        )
        return self._to_create_song_response(song_output)

    def get_song(self, db: Session, song_repo: SongRepository, song_id: int) -> Song:
        song = song_repo.get_song(db, song_id)
        return song_schemas.SongOut(
            id=song.id,
            name=song.name,
            artist_names=[artist.name for artist in song.artists],
            uri=song.uri,
            album_cover=song.album_cover,
            duration=song.duration,
            genre_name=song.genre_name,
            timestamp=song.timestamp,
        )

    def to_get_songs_response(
        self, song_outputs: List[song_schemas.SongOut], song_count: int
    ) -> GetSongsResponse:
        return GetSongsResponse(songs=song_outputs, song_count=song_count)

    def _to_create_song_response(
        self, song_output: song_schemas.Song
    ) -> CreateSongResponse:
        return CreateSongResponse(song=song_output)
