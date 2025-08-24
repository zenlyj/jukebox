from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.database import get_db
from api.responses.PreferenceResponse import AddUserPreferencesResponse
from api.schemas.Preference import PreferenceCreate
from api.repositories import PreferenceRepository
from api.repositories import SongRepository
from api.services import PreferenceService

router = APIRouter()


@router.post("/preference/", response_model=AddUserPreferencesResponse)
def add_user_preferences(
    preference: PreferenceCreate,
    db: Session = Depends(get_db),
    preference_repo: PreferenceRepository = Depends(PreferenceRepository),
    song_repo: SongRepository = Depends(SongRepository),
    preference_service: PreferenceService = Depends(PreferenceService),
):
    return preference_service.create_preferences(
        db, preference_repo, song_repo, preference
    )
