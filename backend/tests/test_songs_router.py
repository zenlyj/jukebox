from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from ..main import app
from .mocks import song_out
from .mocks import song_create


client = TestClient(app)


@pytest.fixture()
def mock_service_get_songs(mocker):
    mocker.patch(
        "api.services.SongService.SongService.get_songs",
        return_value={"songs": [song_out], "song_count": 1},
    )


@pytest.fixture()
def mock_service_get_recommended_songs(mocker):
    mocker.patch(
        "api.services.SongService.SongService.get_recommended_songs",
        return_value={"songs": [song_out], "song_count": 1},
    )


@pytest.fixture()
def mock_service_add_song(mocker):
    mocker.patch(
        "api.services.SongService.SongService.add_song", return_value={"song": song_out}
    )


@pytest.fixture()
def mock_service_add_duplicate_song(mocker):
    mocker.patch(
        "api.services.SongService.SongService.add_song",
        side_effect=HTTPException(status_code=422, detail="Song already created!"),
    )


def test_get_songs_success(mock_service_get_songs):
    response = client.get("/songs/?genre_name=HIPHOP&page_num=1&page_size=10")
    expected_song = song_out.model_dump(mode="json")
    assert response.status_code == 200
    assert response.json() == {"songs": [expected_song], "song_count": 1}


def test_get_songs_missing_genre_fail(mock_service_get_songs):
    response = client.get("/songs/?page_num=1&page_size=10")
    assert response.status_code == 422


def test_get_songs_missing_pagination_fail(mock_service_get_songs):
    response = client.get("/songs/?genre_name=HIPHOP")
    assert response.status_code == 422


def test_get_recommended_songs_success(mock_service_get_recommended_songs):
    response = client.get(
        "/songs/recommendation/?spotify_user_id=123&genre_name=HIPHOP&page_num=1&page_size=10"
    )
    expected_song = song_out.model_dump(mode="json")
    assert response.status_code == 200
    assert response.json() == {"songs": [expected_song], "song_count": 1}


def test_get_recommended_songs_missing_user_id_fail(mock_service_get_recommended_songs):
    response = client.get(
        "/songs/recommendation/?genre_name=HIPHOP&page_num=1&page_size=10"
    )
    assert response.status_code == 422


def test_get_recommended_songs_missing_genre_fail(mock_service_get_recommended_songs):
    response = client.get(
        "/songs/recommendation/?spotify_user_id=123&page_num=1&page_size=10"
    )
    assert response.status_code == 422


def test_get_recommended_songs_missing_pagination_fail(
    mock_service_get_recommended_songs,
):
    response = client.get(
        "/songs/recommendation/?spotify_user_id=123&genre_name=HIPHOP"
    )
    assert response.status_code == 422


def test_add_song_success(mock_service_add_song):
    response = client.post("/songs/", json=song_create.model_dump(mode="json"))
    assert response.status_code == 200
    assert response.json() == {"song": song_out.model_dump(mode="json")}


def test_add_song_invalid_song_create_fail(mock_service_add_song):
    response = client.post("/songs/", json=song_out.model_dump(mode="json"))
    assert response.status_code == 422


def test_add_song_duplicate_song_fail(mock_service_add_duplicate_song):
    response = client.post("/songs/", json=song_create.model_dump(mode="json"))
    assert response.status_code == 422
    assert response.json()["detail"] == "Song already created!"
