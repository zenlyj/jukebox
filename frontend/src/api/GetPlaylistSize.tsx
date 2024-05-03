import { getAccessToken } from "../utils/session.tsx";
import { SERVER_URL } from "./constants.tsx";

export interface GetPlaylistSizeResponse {
  size: number;
}

export async function getPlaylistSize(): Promise<GetPlaylistSizeResponse> {
  return fetch(`${SERVER_URL}/playlist/${getAccessToken()}/size`)
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((data) => ({
      size: data?.size ?? 0,
    }));
}
