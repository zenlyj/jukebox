from fastapi.testclient import TestClient
import pytest
from ..main import app
from .mocks import authorization_create
from .mocks import authorization_refresh
from .mocks import spotify_authorization_response
from .mocks import search_spotify_response
from .mocks import spotify_user_profile_response
from .mocks import spotify_artist_response
from api.exceptions import DomainException
from api.exceptions import ResourceNotFound

client = TestClient(app)


@pytest.fixture()
def mock_service_create_token(mocker):
    return mocker.patch(
        "api.services.SpotifyService.SpotifyService.create_token",
        return_value=spotify_authorization_response,
    )


@pytest.fixture()
def mock_service_refresh_token(mocker):
    return mocker.patch(
        "api.services.SpotifyService.SpotifyService.refresh_token",
        return_value=spotify_authorization_response,
    )


@pytest.fixture()
def mock_service_create_token_unauthorized(mocker):
    mocker.patch(
        "api.services.SpotifyService.SpotifyService.create_token",
        side_effect=DomainException(
            status_code=401, detail="Unauthorized to create Spotify token!"
        ),
    )


@pytest.fixture()
def mock_service_refresh_token_unauthorized(mocker):
    mocker.patch(
        "api.services.SpotifyService.SpotifyService.refresh_token",
        side_effect=DomainException(
            status_code=401, detail="Unauthorized to refresh Spotify token!"
        ),
    )


@pytest.fixture()
def mock_service_search_spotify(mocker):
    mocker.patch(
        "api.services.SpotifyService.SpotifyService.search",
        return_value=search_spotify_response,
    )


@pytest.fixture()
def mock_service_search_spotify_not_found(mocker):
    mocker.patch(
        "api.services.SpotifyService.SpotifyService.search",
        side_effect=ResourceNotFound("Spotify track"),
    )


@pytest.fixture()
def mock_service_get_user_profile_info(mocker):
    mocker.patch(
        "api.services.SpotifyService.SpotifyService.get_user_profile_info",
        return_value=spotify_user_profile_response,
    )


@pytest.fixture()
def mock_service_get_user_profile_info_unauthorized(mocker):
    mocker.patch(
        "api.services.SpotifyService.SpotifyService.get_user_profile_info",
        side_effect=DomainException(
            status_code=401, detail="Unauthorized to get user profile"
        ),
    )


@pytest.fixture()
def mock_service_get_artists(mocker):
    mocker.patch(
        "api.services.SpotifyService.SpotifyService.get_artists",
        return_value=[spotify_artist_response],
    )


@pytest.fixture()
def mock_service_get_artists_unauthorized(mocker):
    mocker.patch(
        "api.services.SpotifyService.SpotifyService.get_artists",
        side_effect=DomainException(
            status_code=401, detail="Unauthorized to get artists"
        ),
    )


def test_authorize_spotify_create_token_success(
    mock_service_create_token, mock_service_refresh_token
):
    response = client.post("/spotify/authorization/", json=authorization_create)
    assert response.status_code == 200
    assert mock_service_create_token.call_count == 1
    assert mock_service_refresh_token.call_count == 0
    assert response.json() == spotify_authorization_response


def test_authorize_spotify_refresh_token_success(
    mock_service_create_token, mock_service_refresh_token
):
    response = client.post("/spotify/authorization/", json=authorization_refresh)
    assert response.status_code == 200
    assert mock_service_create_token.call_count == 0
    assert mock_service_refresh_token.call_count == 1
    assert response.json() == spotify_authorization_response


def test_authorize_spotify_invalid_grant_type_fail(
    mock_service_create_token, mock_service_refresh_token
):
    response = client.post("/spotify/authorization/", json={"grant_type": ""})
    assert response.status_code == 422
    assert mock_service_create_token.call_count == 0
    assert mock_service_refresh_token.call_count == 0


def test_authorize_spotify_create_token_unauthorized_fail(
    mock_service_create_token_unauthorized,
):
    response = client.post("/spotify/authorization/", json=authorization_create)
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized to create Spotify token!"


def test_authorize_spotify_refresh_token_unauthorized_fail(
    mock_service_refresh_token_unauthorized,
):
    response = client.post("/spotify/authorization/", json=authorization_refresh)
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized to refresh Spotify token!"


def test_search_spotify_success(mock_service_search_spotify):
    response = client.get(
        "/spotify/track/?query=stan&query_type=track",
        headers={"Authorization": "Bearer a23fa1"},
    )
    assert response.status_code == 200
    assert response.json() == search_spotify_response


def test_search_spotify_missing_auth_fail(mock_service_search_spotify):
    response = client.get("/spotify/track/?query=stan&query_type=track", headers={})
    assert response.status_code == 422


def test_search_spotify_missing_query_fail(mock_service_search_spotify):
    response = client.get("/spotify/track/", headers={"Authorization": "Bearer a23fa1"})
    assert response.status_code == 422


def test_search_spotify_not_found_fail(mock_service_search_spotify_not_found):
    response = client.get(
        "/spotify/track/?query=stan&query_type=track",
        headers={"Authorization": "Bearer a23fa1"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Spotify track not found"


def test_get_user_profile_success(mock_service_get_user_profile_info):
    response = client.get(
        "/spotify/user-profile/", headers={"Authorization": "Bearer a23fa1"}
    )
    assert response.status_code == 200
    assert response.json() == spotify_user_profile_response


def test_get_user_profile_missing_auth_fail(mock_service_get_user_profile_info):
    response = client.get("/spotify/user-profile/", headers={})
    assert response.status_code == 422


def test_get_user_profile_unauthorized_fail(
    mock_service_get_user_profile_info_unauthorized,
):
    response = client.get(
        "/spotify/user-profile/", headers={"Authorization": "Bearer a23fa1"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized to get user profile"


def test_get_artists_success(mock_service_get_artists):
    response = client.get(
        "/spotify/artists/?ids=1", headers={"Authorization": "Bearer a23fa1"}
    )
    assert response.status_code == 200
    assert response.json() == [spotify_artist_response]


def test_get_artists_missing_ids_fail(mock_service_get_artists):
    response = client.get(
        "/spotify/artists/", headers={"Authorization": "Bearer a23fa1"}
    )
    assert response.status_code == 422


def test_get_artists_missing_auth_fail(mock_service_get_artists):
    response = client.get("/spotify/artists/?ids=1", headers={})
    assert response.status_code == 422


def test_get_artists_unauthorized_fail(mock_service_get_artists_unauthorized):
    response = client.get(
        "/spotify/artists/?ids=1", headers={"Authorization": "Bearer a23fa1"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized to get artists"
