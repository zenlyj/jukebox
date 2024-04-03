import { Song, SongInput, inputToSong } from "../components/models/Song.tsx";
import { SERVER_URL, accessToken } from "./constants.tsx";

export interface GetPlaylistResponse {
  songs: Song[];
}

export async function getPlaylist(): Promise<GetPlaylistResponse> {
  return fetch(`${SERVER_URL}/playlist/${accessToken()}`)
    .then((response: Response) => (response.ok ? response.json() : []))
    .then((inputs: SongInput[]) => ({
      songs: inputs.map((input) => inputToSong(input)),
    }));
}
