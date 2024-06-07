from api.schemas.Song import SongOut
from api.schemas.Song import SongCreate
from api.schemas.Artist import ArtistCreate
from api.schemas.Playlist import PlaylistCreate
from api.schemas.Preference import PreferenceCreate

song_out = SongOut(
    id=1,
    name="runaway",
    artist_names=["kanye west"],
    uri="",
    album_cover="",
    duration=123456,
    genre_name="HIP_HOP",
    timestamp="123456",
)

song_create = SongCreate(
    name="swimming pools (drank)",
    uri="",
    album_cover="",
    duration=123456,
    spotify_id="123",
    genre_name="HIPHOP",
    timestamp="123456",
    artists=[
        ArtistCreate(name="kendrick lamar", spotify_id="123", genres=["west coast rap"])
    ],
)

playlist_create = PlaylistCreate(spotify_user_id="123", song_id=1)

preference_create = PreferenceCreate(song_id=1, spotify_user_id="123")
