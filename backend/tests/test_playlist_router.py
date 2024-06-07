from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from ..main import app
from .mocks import song_out
from .mocks import playlist_create

client = TestClient(app)


@pytest.fixture()
def mock_service_get_playlist_songs(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.get_playlist_songs",
        return_value={"songs": [song_out], "song_count": 1},
    )


@pytest.fixture()
def mock_service_get_playlist_size(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.get_playlist_size",
        return_value={"size": 1, "message": "1 song in playlist"},
    )


@pytest.fixture()
def mock_service_add_song_to_playlist(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.add_song_to_playlist",
        return_value={
            "id": 1,
            "spotify_user_id": "123",
            "song_id": 1,
            "message": "Successfully added to playlist!",
        },
    )


@pytest.fixture()
def mock_service_add_duplicate_song_to_playlist(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.add_song_to_playlist",
        side_effect=HTTPException(
            status_code=422, detail="Song already added to playlist!"
        ),
    )


@pytest.fixture()
def mock_service_remove_song_from_playlist(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.remove_song_from_playlist",
        return_value={"message": "Successfully deleted song 1 from playlist!"},
    )


@pytest.fixture()
def mock_service_remove_song_from_playlist_not_found(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.remove_song_from_playlist",
        side_effect=HTTPException(status_code=422, detail="Failed to delete song"),
    )


def test_get_playlist_songs_success(mock_service_get_playlist_songs):
    response = client.get("/playlist/?spotify_user_id=123&page_num=1&page_size=10")
    expected_song = song_out.model_dump(mode="json")
    assert response.status_code == 200
    assert response.json() == {"songs": [expected_song], "song_count": 1}


def test_get_playlist_songs_missing_spotify_user_id_fail(
    mock_service_get_playlist_songs,
):
    response = client.get("/playlist/?page_num=1&page_size=10")
    assert response.status_code == 422


def test_get_playlist_songs_missing_pagination_fail(mock_service_get_playlist_songs):
    response = client.get("/playlist/?spotify_user_id=123")
    assert response.status_code == 422


def test_get_playlist_size_success(mock_service_get_playlist_size):
    response = client.get("/playlist/size/?spotify_user_id=123")
    assert response.status_code == 200
    assert response.json() == {"size": 1, "message": "1 song in playlist"}


def test_get_playlist_size_missing_spotify_user_id_fail(mock_service_get_playlist_size):
    response = client.get("/playlist/size/")
    assert response.status_code == 422


def test_add_song_to_playlist_success(mock_service_add_song_to_playlist):
    response = client.post("/playlist/", json=playlist_create.model_dump(mode="json"))
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "spotify_user_id": "123",
        "song_id": 1,
        "message": "Successfully added to playlist!",
    }


def test_add_song_to_playlist_invalid_playlist_create_fail(
    mock_service_add_song_to_playlist,
):
    response = client.post("/playlist/", json={"song_id": 1})
    assert response.status_code == 422


def test_add_song_to_playlist_duplicate_song_fail(
    mock_service_add_duplicate_song_to_playlist,
):
    response = client.post("/playlist/", json=playlist_create.model_dump(mode="json"))
    assert response.status_code == 422
    assert response.json()["detail"] == "Song already added to playlist!"


def test_remove_song_from_playlist(mock_service_remove_song_from_playlist):
    response = client.delete("/playlist/?spotify_user_id=123&song_id=1")
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully deleted song 1 from playlist!"}


def test_remove_song_from_playlist_missing_spotify_user_id_fail(
    mock_service_remove_song_from_playlist,
):
    response = client.delete("/playlist/?song_id=1")
    assert response.status_code == 422


def test_remove_song_from_playlist_missing_song_id_fail(
    mock_service_remove_song_from_playlist,
):
    response = client.delete("/playlist/?spotify_user_id=123")
    assert response.status_code == 422


def test_remove_song_from_playlist_not_found(
    mock_service_remove_song_from_playlist_not_found,
):
    response = client.delete("/playlist/?spotify_user_id=123&song_id=1")
    assert response.status_code == 422
    assert response.json()["detail"] == "Failed to delete song"
