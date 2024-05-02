import { SERVER_URL, refreshToken, expireTime } from "./constants.tsx";

interface ServerResponse {
  access_token: string | null;
}

const mapResponse = (response: ServerResponse): RefreshAccessTokenResponse => ({
  accessToken: response.access_token,
});

export interface RefreshAccessTokenResponse {
  accessToken: string | null;
}

export async function refreshAccessToken(
  accessToken: string
): Promise<RefreshAccessTokenResponse> {
  const url =
    `${SERVER_URL}/spotify/authorize/refresh/?` +
    new URLSearchParams({
      expired_token: accessToken,
      refresh_token: refreshToken() ?? "",
    });
  return fetch(url)
    .then((response: Response) =>
      response.ok ? response.json() : { access_token: null }
    )
    .then((response: ServerResponse) => mapResponse(response));
}
