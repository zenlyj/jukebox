import { Song, SongInput, inputToSong } from "../components/models/Song.tsx";
import { SERVER_URL } from "./constants.tsx";

export interface GetSongsResponse {
  songs: Song[];
}

export async function getSongs(): Promise<GetSongsResponse> {
  return fetch(`${SERVER_URL}/songs/`)
    .then((response: Response) => (response.ok ? response.json() : []))
    .then((inputs: SongInput[]) => ({
      songs: inputs.map((input) => inputToSong(input)),
    }));
}
