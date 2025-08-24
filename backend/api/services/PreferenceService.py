from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from api.repositories import PreferenceRepository
from api.repositories import SongRepository
from api.models import Preference
from api.schemas import Preference as preference_schemas
from api.responses.PreferenceResponse import AddUserPreferencesResponse
from api.responses.PreferenceResponse import GetUserPreferencesResponse
from api.exceptions import ResourceNotFound


class PreferenceService:
    def create_preferences(
        self,
        db: Session,
        preference_repo: PreferenceRepository,
        song_repo: SongRepository,
        preference: preference_schemas.PreferenceCreate,
    ) -> AddUserPreferencesResponse:
        try:
            song = song_repo.get_song(db, preference.song_id)
        except NoResultFound:
            raise ResourceNotFound("Preferred song")

        spotify_user_id = preference.spotify_user_id
        curr_preferences = set(
            [
                (pref.artist_genre_id, pref.spotify_user_id)
                for pref in preference_repo.get_user_preferences(db, spotify_user_id)
            ]
        )
        artist_genre_ids = [
            genre.id for artist in song.artists for genre in artist.artist_genres
        ]
        new_preferences = [
            Preference(spotify_user_id=spotify_user_id, artist_genre_id=artist_genre_id)
            for artist_genre_id in artist_genre_ids
            if (artist_genre_id, spotify_user_id) not in curr_preferences
        ]
        preference_repo.add_user_preferences(db, new_preferences)
        return AddUserPreferencesResponse(
            spotify_user_id=spotify_user_id,
            artist_genre_ids=artist_genre_ids,
        )

    def get_preferences(
        self, db: Session, preference_repo: PreferenceRepository, spotify_user_id: str
    ) -> GetUserPreferencesResponse:
        preferences = preference_repo.get_user_preferences(db, spotify_user_id)
        return GetUserPreferencesResponse(
            spotify_user_id=spotify_user_id,
            artist_genre_ids=[preference.artist_genre_id for preference in preferences],
        )
