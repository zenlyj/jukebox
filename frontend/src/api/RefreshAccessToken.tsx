import { getRefreshToken } from "../utils/session.tsx";
import { SERVER_URL } from "./constants.tsx";

interface ServerResponse {
  access_token: string;
  expires_in: number;
}

const mapServerResponse = (
  response: ServerResponse | null
): RefreshAccessTokenResponse =>
  !response
    ? { accessToken: null, expiresIn: null }
    : {
        accessToken: response.access_token,
        expiresIn: response.expires_in,
      };

export interface RefreshAccessTokenResponse {
  accessToken: string | null;
  expiresIn: number | null;
}

export async function refreshAccessToken(
  accessToken: string
): Promise<RefreshAccessTokenResponse> {
  const url =
    `${SERVER_URL}/spotify/authorize/refresh/?` +
    new URLSearchParams({
      expired_token: accessToken,
      refresh_token: getRefreshToken() ?? "",
    });
  return fetch(url)
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((response: ServerResponse | null) => mapServerResponse(response));
}
