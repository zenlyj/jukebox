import { SERVER_URL } from "./constants.tsx";

export interface AddSongToPlaylistResponse {
  isAdded: boolean;
}

export async function addSongToPlaylist(
  spotifyUserId: string,
  songId: number
): Promise<AddSongToPlaylistResponse> {
  return fetch(`${SERVER_URL}/playlist/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      spotify_user_id: spotifyUserId,
      song_id: songId,
    }),
  }).then((response: Response) => ({ isAdded: response.ok }));
}
