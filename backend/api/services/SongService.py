from sqlalchemy.orm import Session
from typing import List, Tuple
from api.repositories import SongRepository
from api.repositories import PreferenceRepository
from api.responses.SongResponse import GetSongsResponse
from api.responses.SongResponse import CreateSongResponse
from api.schemas import Song as song_schemas
from api.models import Song
from api.models import Artist
from api.models import ArtistGenre
from api.tools.algorithms import preference_score
from api.exceptions import ResourceAlreadyExists


class SongService:
    def get_songs(
        self,
        db: Session,
        song_repo: SongRepository,
        genre_name: str,
        page_num: int,
        page_size: int,
    ) -> GetSongsResponse:
        offset, limit = self._get_offset_and_limit(page_num, page_size)
        songs = song_repo.get_songs_ordered_by_date(db, genre_name, offset, limit)
        song_count = song_repo.get_song_count(db, genre_name)
        return self.to_get_songs_response(songs, song_count)

    def get_recommended_songs(
        self,
        db: Session,
        song_repo: SongRepository,
        pref_repo: PreferenceRepository,
        spotify_user_id: str,
        genre_name: str,
        page_num: int,
        page_size: int,
    ) -> GetSongsResponse:
        offset, limit = self._get_offset_and_limit(page_num, page_size)
        songs = song_repo.get_all_songs(db, genre_name)
        user_preferred_genres = set(
            genre.name
            for pref in pref_repo.get_user_preferences(db, spotify_user_id)
            for genre in pref.artist_genres
        )
        all_genres = set(
            genre.name
            for song in songs
            for artist in song.artists
            for genre in artist.artist_genres
        )
        recommendation = []
        id_to_song_mapping = {}
        for song in songs:
            song_genres = set(
                genre.name for artist in song.artists for genre in artist.artist_genres
            )
            score = preference_score(all_genres, user_preferred_genres, song_genres)
            recommendation.append((score, song.id))
            id_to_song_mapping.setdefault(song.id, song)
        recommendation = [
            id
            for _, id in sorted(recommendation, reverse=True)[offset : offset + limit]
        ]
        recommended_songs = [id_to_song_mapping[song_id] for song_id in recommendation]
        song_count = song_repo.get_song_count(db, genre_name)
        return self.to_get_songs_response(recommended_songs, song_count)

    def add_song(
        self, db: Session, song_repo: SongRepository, song: song_schemas.SongCreate
    ) -> CreateSongResponse:
        if song_repo.is_song_exist(db, song.spotify_id):
            raise ResourceAlreadyExists("Song")
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
        return self._to_create_song_response(new_song)

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
        self, songs: List[Song], song_count: int
    ) -> GetSongsResponse:
        song_outputs = [self._to_song_out(song) for song in songs]
        return GetSongsResponse(songs=song_outputs, song_count=song_count)

    def _to_create_song_response(self, song: Song) -> CreateSongResponse:
        song_output = self._to_song_out(song)
        return CreateSongResponse(song=song_output)

    def _to_song_out(self, song: Song) -> song_schemas.SongOut:
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

    def _get_offset_and_limit(self, page_num: int, page_size: int) -> Tuple[int, int]:
        return (page_num - 1) * page_size, page_size
