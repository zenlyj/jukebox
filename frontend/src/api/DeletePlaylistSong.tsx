import { getAccessToken } from "../utils/session.tsx";
import { SERVER_URL } from "./constants.tsx";

export interface DeletePlaylistSongResponse {
  isDeleted: boolean;
}

export async function deletePlaylistSong(
  songId: number
): Promise<DeletePlaylistSongResponse> {
  return fetch(`${SERVER_URL}/playlist/${getAccessToken()}/${songId}`, {
    method: "DELETE",
  }).then((response: Response) => ({ isDeleted: response.ok }));
}
