import { SERVER_URL, accessToken } from "./constants.tsx";

export interface DeletePlaylistSongResponse {
  isDeleted: boolean;
}

export async function deletePlaylistSong(
  songId: number
): Promise<DeletePlaylistSongResponse> {
  return fetch(
    `${SERVER_URL}/playlist/?session=${accessToken()}&song_id=${songId}`,
    {
      method: "DELETE",
    }
  ).then((response: Response) => ({ isDeleted: response.ok }));
}
