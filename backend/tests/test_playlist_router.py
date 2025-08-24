from fastapi.testclient import TestClient
import pytest
from ..main import app
from .mocks import playlist_create
from .mocks import get_songs_response
from .mocks import get_playlist_size_response
from .mocks import add_song_to_playlist_response
from .mocks import delete_song_from_playlist_response
from api.exceptions import ResourceAlreadyExists
from api.exceptions import ResourceNotFound

client = TestClient(app)


@pytest.fixture()
def mock_service_get_playlist_songs(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.get_playlist_songs",
        return_value=get_songs_response,
    )


@pytest.fixture()
def mock_service_get_playlist_size(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.get_playlist_size",
        return_value=get_playlist_size_response,
    )


@pytest.fixture()
def mock_service_add_song_to_playlist(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.add_song_to_playlist",
        return_value=add_song_to_playlist_response,
    )


@pytest.fixture()
def mock_service_add_duplicate_song_to_playlist(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.add_song_to_playlist",
        side_effect=ResourceAlreadyExists("Playlist song"),
    )


@pytest.fixture()
def mock_service_remove_song_from_playlist(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.remove_song_from_playlist",
        return_value=delete_song_from_playlist_response,
    )


@pytest.fixture()
def mock_service_remove_song_from_playlist_not_found(mocker):
    mocker.patch(
        "api.services.PlaylistService.PlaylistService.remove_song_from_playlist",
        side_effect=ResourceNotFound("Playlist song"),
    )


def test_get_playlist_songs_success(mock_service_get_playlist_songs):
    response = client.get("/playlist/?spotify_user_id=123&page_num=1&page_size=10")
    assert response.status_code == 200
    assert response.json() == get_songs_response


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
    assert response.json() == get_playlist_size_response


def test_get_playlist_size_missing_spotify_user_id_fail(mock_service_get_playlist_size):
    response = client.get("/playlist/size/")
    assert response.status_code == 422


def test_add_song_to_playlist_success(mock_service_add_song_to_playlist):
    response = client.post("/playlist/", json=playlist_create)
    assert response.status_code == 200
    assert response.json() == add_song_to_playlist_response


def test_add_song_to_playlist_invalid_playlist_create_fail(
    mock_service_add_song_to_playlist,
):
    response = client.post("/playlist/", json={"song_id": 1})
    assert response.status_code == 422


def test_add_song_to_playlist_duplicate_song_fail(
    mock_service_add_duplicate_song_to_playlist,
):
    response = client.post("/playlist/", json=playlist_create)
    assert response.status_code == 409
    assert response.json()["detail"] == "Playlist song already exists"


def test_remove_song_from_playlist_success(mock_service_remove_song_from_playlist):
    response = client.delete("/playlist/?spotify_user_id=123&song_id=1")
    assert response.status_code == 200
    assert response.json() == delete_song_from_playlist_response


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


def test_remove_song_from_playlist_not_found_fail(
    mock_service_remove_song_from_playlist_not_found,
):
    response = client.delete("/playlist/?spotify_user_id=123&song_id=1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Playlist song not found"
