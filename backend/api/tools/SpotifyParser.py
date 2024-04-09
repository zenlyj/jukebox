import json
from .algorithms import similarity
from typing import List
from typing import Union
from .DataTypes import SpotifyData

class SpotifyParser():
    def parse_spotify_search(self, result_text: str, query: str) -> Union[SpotifyData, None]:
        result: dict = json.loads(result_text)
        tracks_key, items_key = 'tracks', 'items'
        key_not_found = (tracks_key not in result) or (items_key not in result[tracks_key])
        return self.__get_best_result(result[tracks_key][items_key], query) if not key_not_found else None

    def __get_best_result(self, tracks_data: dict, query: str) -> Union[SpotifyData, None]:
        def to_comparison_text(spotify_data: SpotifyData):
            name, artist_names = spotify_data[0], spotify_data[1]
            return ' '.join([name] + artist_names)
        
        spotify_datas = [self.__extract(track_data) for track_data in tracks_data]
        comparison_texts = [to_comparison_text(spotify_data) for spotify_data in spotify_datas]
        similarities = [similarity(query, comparison_text) for comparison_text in comparison_texts]
        candidates = [spotify_data for spotify_data, similarity in zip(spotify_datas, similarities) if similarity == max(similarities)]
        return candidates[0] if len(candidates) > 0 else None

    def __extract(self, track_data: dict) -> SpotifyData:
        name = self.__extract_name(track_data)
        artist_names = self.__extract_artist_names(track_data)
        uri = self.__extract_uri(track_data)
        album_cover = self.__extract_album_cover(track_data)
        duration = self.__extract_duration(track_data)
        spotify_id = self.__extract_spotify_id(track_data)
        return name, artist_names, uri, album_cover, duration, spotify_id

    def __extract_name(self, track_data: dict) -> Union[str, None]:
        name_key = 'name'
        return track_data[name_key] if name_key in track_data else None
    
    def __extract_artist_names(self, track_data: dict) -> List[str]:
        artists_key, artist_name_key = 'artists', 'name'
        key_not_found = (artists_key not in track_data) or \
            (len(track_data[artists_key]) == 0) or \
            (artist_name_key not in track_data[artists_key][0])
        if key_not_found:
            return []
        artist_names = [artist[artist_name_key] for artist in track_data[artists_key]]
        return artist_names

    def __extract_uri(self, track_data: dict) -> Union[str, None]:
        uri_key = 'uri'
        return track_data[uri_key] if uri_key in track_data else None
    
    def __extract_album_cover(self, track_data: dict) -> Union[str, None]:
        album_key, images_key, url_key = 'album', 'images', 'url'
        key_not_found = (album_key not in track_data) or \
            (images_key not in track_data[album_key]) or \
            (len(track_data[album_key][images_key]) == 0) or \
            (url_key not in track_data[album_key][images_key][0])
        return track_data[album_key][images_key][0][url_key] if not key_not_found else None
    
    def __extract_duration(self, track_data: dict) -> Union[str, None]:
        duration_key = 'duration_ms'
        return track_data[duration_key] if duration_key in track_data else None
    
    def __extract_spotify_id(self, track_data: dict) -> Union[str, None]:
        id_key = 'id'
        return track_data[id_key] if id_key in track_data else None
