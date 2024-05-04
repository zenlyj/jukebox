import { SERVER_URL } from "./constants.tsx";

export interface DeletePlaylistSongResponse {
  isDeleted: boolean;
}

export async function deletePlaylistSong(
  spotifyUserId: string,
  songId: number
): Promise<DeletePlaylistSongResponse> {
  const url =
    `${SERVER_URL}/playlist/?` +
    new URLSearchParams({
      spotify_user_id: spotifyUserId,
      song_id: `${songId}`,
    });
  return fetch(url, {
    method: "DELETE",
  }).then((response: Response) => ({ isDeleted: response.ok }));
}
