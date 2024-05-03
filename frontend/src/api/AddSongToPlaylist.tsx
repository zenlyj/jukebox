import { getAccessToken } from "../utils/session.tsx";
import { SERVER_URL } from "./constants.tsx";

export interface AddSongToPlaylistResponse {
  isAdded: boolean;
}

export async function addSongToPlaylist(
  songId: number
): Promise<AddSongToPlaylistResponse> {
  return fetch(`${SERVER_URL}/playlist/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session: getAccessToken(),
      song: songId,
    }),
  }).then((response: Response) => ({ isAdded: response.ok }));
}
