import { SERVER_URL, accessToken } from "./constants.tsx";

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
      session: accessToken(),
      song: songId,
    }),
  }).then((response: Response) => ({ isAdded: response.ok }));
}
