from sqlalchemy.orm import Session
from typing import List

from api.models import Preference


class PreferenceRepository:
    def add_user_preferences(self, db: Session, preferences: List[Preference]) -> None:
        db.add_all(preferences)
        db.commit()
        for preference in preferences:
            db.refresh(preference)

    def get_user_preferences(
        self, db: Session, spotify_user_id: str
    ) -> List[Preference]:
        return (
            db.query(Preference)
            .filter(Preference.spotify_user_id == spotify_user_id)
            .all()
        )
