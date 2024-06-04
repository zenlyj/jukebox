from fastapi.testclient import TestClient
from ..main import app
from api.schemas.Song import SongOut

client = TestClient(app)


def test(mocker):
    mock_song = SongOut(
        id=1,
        name="runaway",
        artist_names=["kanye west"],
        uri="",
        album_cover="",
        duration="123456",
        genre_name="HIP_HOP",
        timestamp="123456",
    )
    mocker.patch(
        "api.services.SongService.SongService.get_songs",
        return_value={"songs": [mock_song], "song_count": 1},
    )
    response = client.get("/songs/?genre_name=HIP_HOP&page_num=1&page_size=10")
    assert response.status_code == 200
    expected_song = mock_song.model_dump(mode="json")
    assert response.json() == {"songs": [expected_song], "song_count": 1}
