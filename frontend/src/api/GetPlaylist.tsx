import { Genre } from "../components/models/Genre.tsx";
import { Song } from "../components/models/Song.tsx";
import { getAccessToken } from "../utils/session.tsx";
import { SERVER_URL } from "./constants.tsx";

export interface GetPlaylistResponse {
  songs: Song[];
  playlistSize: number;
}

export interface ServerResponse {
  songs: {
    id: number;
    name: string;
    artist_names: string[];
    uri: string;
    album_cover: string;
    duration: number;
    genre_name: Genre;
    timestamp: string;
  }[];
  song_count: number;
}

const mapServerResponse = (
  response: ServerResponse | null
): GetPlaylistResponse => {
  if (!response) {
    return {
      songs: [],
      playlistSize: 0,
    };
  }
  const songs = response.songs.map((song) => ({
    id: song.id,
    name: song.name,
    artistNames: song.artist_names,
    uri: song.uri,
    albumCover: song.album_cover,
    duration: song.duration,
    genreName: song.genre_name,
    timestamp: song.timestamp,
  }));
  return {
    songs: songs,
    playlistSize: response.song_count,
  };
};

export async function getPlaylist(
  pageNumber: number,
  pageSize: number
): Promise<GetPlaylistResponse> {
  const url =
    `${SERVER_URL}/playlist/${getAccessToken()}/?` +
    new URLSearchParams({
      page_num: `${pageNumber}`,
      page_size: `${pageSize}`,
    });
  return fetch(url)
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((response: ServerResponse | null) => mapServerResponse(response));
}
