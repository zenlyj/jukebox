import { Song } from "../components/models/Song";
import { SERVER_URL, accessToken } from "./constants.tsx";

export interface GetPlaylistResponse {
  songs: Song[];
}

export async function getPlaylist(): Promise<GetPlaylistResponse> {
  return fetch(`${SERVER_URL}/playlist/?session=${accessToken()}`)
    .then((response: Response) => (response.ok ? response.json() : []))
    .then((songs: Song[]) => ({ songs: songs }));
}
