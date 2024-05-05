import json
from .algorithms import similarity
from typing import List
from typing import Union
from .DataTypes import SpotifySearchTrackData
from .DataTypes import SpotifySearchTrackArtistData
from .DataTypes import SpotifyArtistData


class SpotifyParser:
    def parse_spotify_search(
        self, result_text: str, query: str
    ) -> Union[SpotifySearchTrackData, None]:
        result: dict = json.loads(result_text)
        tracks_key, items_key = "tracks", "items"
        key_not_found = (tracks_key not in result) or (
            items_key not in result[tracks_key]
        )
        return (
            self.__get_best_result(result[tracks_key][items_key], query)
            if not key_not_found
            else None
        )

    def parse_spotify_artists(self, result_text: str) -> List[SpotifyArtistData]:
        result: dict = json.loads(result_text)
        artists_key = "artists"
        if artists_key not in result:
            return []
        artists_data = result[artists_key]
        res = []
        for artist_data in artists_data:
            name = self.__extract_artist_name(artist_data)
            genres = self.__extract_artist_genres(artist_data)
            spotify_id = self.__extract_artist_spotify_id(artist_data)
            res.append((name, genres, spotify_id))
        return res

    def __get_best_result(
        self, tracks_data: dict, query: str
    ) -> Union[SpotifySearchTrackData, None]:
        def to_comparison_text(spotify_data: SpotifySearchTrackData):
            name, artist_names = spotify_data[0], [
                artist[0] for artist in spotify_data[1]
            ]
            return " ".join([name] + artist_names)

        spotify_datas = [
            self.__extract_track_data(track_data) for track_data in tracks_data
        ]
        comparison_texts = [
            to_comparison_text(spotify_data) for spotify_data in spotify_datas
        ]
        similarities = [
            similarity(query, comparison_text) for comparison_text in comparison_texts
        ]
        candidates = [
            spotify_data
            for spotify_data, similarity in zip(spotify_datas, similarities)
            if similarity == max(similarities)
        ]
        return candidates[0] if len(candidates) > 0 else None

    def __extract_track_data(self, track_data: dict) -> SpotifySearchTrackData:
        name = self.__extract_track_name(track_data)
        artists = self.__extract_track_artists(track_data)
        uri = self.__extract_track_uri(track_data)
        album_cover = self.__extract_track_album_cover(track_data)
        duration = self.__extract_track_duration(track_data)
        spotify_id = self.__extract_track_spotify_id(track_data)
        return name, artists, uri, album_cover, duration, spotify_id

    def __extract_track_name(self, track_data: dict) -> Union[str, None]:
        name_key = "name"
        return track_data[name_key] if name_key in track_data else None

    def __extract_track_artists(
        self, track_data: dict
    ) -> List[SpotifySearchTrackArtistData]:
        artists_key = "artists"
        if artists_key not in track_data:
            return []
        artists_data = track_data[artists_key]
        res: List[SpotifySearchTrackArtistData] = []
        for artist_data in artists_data:
            name = self.__extract_track_artist_name(artist_data)
            id = self.__extract_track_artist_spotify_id(artist_data)
            res.append((name, id))
        return res

    def __extract_track_artist_name(self, artist_data: dict) -> Union[str, None]:
        artist_name_key = "name"
        return artist_data[artist_name_key] if artist_name_key in artist_data else None

    def __extract_track_artist_spotify_id(self, artist_data: dict) -> Union[str, None]:
        artist_genres_key = "id"
        return (
            artist_data[artist_genres_key] if artist_genres_key in artist_data else []
        )

    def __extract_track_uri(self, track_data: dict) -> Union[str, None]:
        uri_key = "uri"
        return track_data[uri_key] if uri_key in track_data else None

    def __extract_track_album_cover(self, track_data: dict) -> Union[str, None]:
        album_key, images_key, url_key = "album", "images", "url"
        key_not_found = (
            (album_key not in track_data)
            or (images_key not in track_data[album_key])
            or (len(track_data[album_key][images_key]) == 0)
            or (url_key not in track_data[album_key][images_key][0])
        )
        return (
            track_data[album_key][images_key][0][url_key] if not key_not_found else None
        )

    def __extract_track_duration(self, track_data: dict) -> Union[str, None]:
        duration_key = "duration_ms"
        return track_data[duration_key] if duration_key in track_data else None

    def __extract_track_spotify_id(self, track_data: dict) -> Union[str, None]:
        id_key = "id"
        return track_data[id_key] if id_key in track_data else None

    def __extract_artist_name(self, artist_data: dict) -> Union[str, None]:
        artist_name_key = "name"
        return artist_data[artist_name_key] if artist_name_key in artist_data else None

    def __extract_artist_genres(self, artist_data: dict) -> List[str]:
        artist_genres_key = "genres"
        return (
            artist_data[artist_genres_key] if artist_genres_key in artist_data else []
        )

    def __extract_artist_spotify_id(self, artist_data: dict) -> Union[str, None]:
        artist_spotify_id_key = "id"
        return (
            artist_data[artist_spotify_id_key]
            if artist_spotify_id_key in artist_data
            else None
        )
