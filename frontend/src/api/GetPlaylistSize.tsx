import { SERVER_URL, accessToken } from "./constants.tsx";

export interface GetPlaylistSizeResponse {
  size: number;
}

export async function getPlaylistSize(): Promise<GetPlaylistSizeResponse> {
  return fetch(`${SERVER_URL}/playlist/${accessToken()}/size`)
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((data) => ({
      size: data?.size ?? 0,
    }));
}
