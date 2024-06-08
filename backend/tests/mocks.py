from api.schemas.Song import SongOut
from api.schemas.Song import SongCreate
from api.schemas.Artist import ArtistCreate
from api.schemas.Playlist import PlaylistCreate
from api.schemas.Preference import PreferenceCreate
from api.schemas.Authorization import AuthorizationCreate
from api.schemas.Authorization import AuthorizationRefresh
from api.responses.PreferenceResponse import AddUserPreferencesResponse
from api.responses.SongResponse import GetSongsResponse
from api.responses.SongResponse import CreateSongResponse
from api.responses.PlaylistResponse import GetPlaylistSizeResponse
from api.responses.PlaylistResponse import AddSongToPlaylistResponse
from api.responses.PlaylistResponse import DeleteSongFromPlaylistResponse
from api.responses.SpotifyResponse import SpotifyAuthorizationResponse
from api.responses.SpotifyResponse import SearchSpotifyResponse
from api.responses.SpotifyResponse import SpotifyUserProfileResponse
from api.responses.SpotifyResponse import SpotifyArtistResponse


song_out = SongOut(
    id=1,
    name="runaway",
    artist_names=["kanye west"],
    uri="",
    album_cover="",
    duration=123456,
    genre_name="HIP_HOP",
    timestamp="123456",
).model_dump(mode="json")

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
).model_dump(mode="json")

playlist_create = PlaylistCreate(spotify_user_id="123", song_id=1).model_dump(
    mode="json"
)

preference_create = PreferenceCreate(song_id=1, spotify_user_id="123").model_dump(
    mode="json"
)

authorization_create = AuthorizationCreate(
    grant_type="authorization_code", authorization_code="123"
).model_dump(mode="json")

authorization_refresh = AuthorizationRefresh(
    grant_type="refresh_token", access_token="123", refresh_token="123"
).model_dump(mode="json")

add_user_preferences_response = AddUserPreferencesResponse(
    spotify_user_id="123",
    artist_genre_ids=[1, 2, 3],
    message="Successfully added user preferences!",
).model_dump(mode="json")

get_songs_response = GetSongsResponse(songs=[song_out], song_count=1).model_dump(
    mode="json"
)

create_song_response = CreateSongResponse(song=song_out).model_dump(mode="json")

get_playlist_size_response = GetPlaylistSizeResponse(
    size=1, message="1 song in playlist"
).model_dump(mode="json")

add_song_to_playlist_response = AddSongToPlaylistResponse(
    id=1, spotify_user_id="123", song_id=1, message="Successfully added to playlist!"
).model_dump(mode="json")

delete_song_from_playlist_response = DeleteSongFromPlaylistResponse(
    message="Successfully deleted song 1 from playlist!"
).model_dump(mode="json")


spotify_authorization_response = SpotifyAuthorizationResponse(
    access_token="123", refresh_token="123", expires_in=99999
).model_dump(mode="json")

search_spotify_response = SearchSpotifyResponse(
    name="family matters",
    artists_spotify_id=["1", "2", "3"],
    uri="",
    album_cover="",
    duration=123456,
    spotify_id="123",
).model_dump(mode="json")

spotify_user_profile_response = SpotifyUserProfileResponse(
    name="zenlyj", user_id="97"
).model_dump(mode="json")

spotify_artist_response = SpotifyArtistResponse(
    name="eminem", genres=["poetry", "lyrics rap"], spotify_id="123"
).model_dump(mode="json")
