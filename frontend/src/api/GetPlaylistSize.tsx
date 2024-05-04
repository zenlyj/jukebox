import { SERVER_URL } from "./constants.tsx";

export interface GetPlaylistSizeResponse {
  size: number;
}

export async function getPlaylistSize(
  spotifyUserId: string
): Promise<GetPlaylistSizeResponse> {
  const url =
    `${SERVER_URL}/playlist/size/?` +
    new URLSearchParams({
      spotify_user_id: spotifyUserId,
    });
  return fetch(url)
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((data) => ({
      size: data?.size ?? 0,
    }));
}
