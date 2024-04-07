import { Genre } from "../components/models/Genre.tsx";
import { Song, SongInput, inputToSong } from "../components/models/Song.tsx";
import { SERVER_URL } from "./constants.tsx";

export interface GetSongsResponse {
  songs: Song[];
}

export async function getSongs(genre: Genre): Promise<GetSongsResponse> {
  const url =
    `${SERVER_URL}/songs/?` +
    new URLSearchParams({
      genre_name: genre,
    });
  return fetch(url)
    .then((response: Response) => (response.ok ? response.json() : []))
    .then((inputs: SongInput[]) => ({
      songs: inputs.map((input) => inputToSong(input)),
    }));
}
