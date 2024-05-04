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
  accessToken: string,
  refreshToken: string
): Promise<RefreshAccessTokenResponse> {
  return fetch(`${SERVER_URL}/spotify/authorization/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      grant_type: "refresh_token",
      access_token: accessToken,
      refresh_token: refreshToken,
    }),
  })
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((response: ServerResponse | null) => mapServerResponse(response));
}
