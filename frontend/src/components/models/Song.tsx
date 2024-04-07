import { Genre } from "./Genre";

export interface Song {
  id: number;
  name: string;
  artistNames: string[];
  uri: string;
  albumCover: string;
  duration: number;
  genreName: Genre;
}

export interface SongInput {
  id: number;
  name: string;
  artist_names: string[];
  uri: string;
  album_cover: string;
  duration: number;
  genre_name: Genre;
}

export function inputToSong(input: SongInput): Song {
  return {
    id: input.id,
    name: input.name,
    artistNames: input.artist_names,
    uri: input.uri,
    albumCover: input.album_cover,
    duration: input.duration,
    genreName: input.genre_name,
  };
}
