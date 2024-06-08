from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from ..main import app
from .mocks import preference_create
from .mocks import add_user_preferences_response

client = TestClient(app)


@pytest.fixture()
def mock_service_create_preferences(mocker):
    mocker.patch(
        "api.services.PreferenceService.PreferenceService.create_preferences",
        return_value=add_user_preferences_response,
    )


@pytest.fixture()
def mock_service_create_preferences_song_not_found(mocker):
    mocker.patch(
        "api.services.PreferenceService.PreferenceService.create_preferences",
        side_effect=HTTPException(status_code=400, detail="No such song!"),
    )


def test_add_user_preferences_success(mock_service_create_preferences):
    response = client.post("/preference/", json=preference_create)
    assert response.status_code == 200
    assert response.json() == add_user_preferences_response


def test_add_user_preferences_invalid_preferences_create_fail(
    mock_service_create_preferences,
):
    response = client.post("/preference/", json={"spotify_user_id": "123"})
    assert response.status_code == 422


def test_add_user_preferences_song_not_found_fail(
    mock_service_create_preferences_song_not_found,
):
    response = client.post("/preference/", json=preference_create)
    assert response.status_code == 400
    assert response.json()["detail"] == "No such song!"
