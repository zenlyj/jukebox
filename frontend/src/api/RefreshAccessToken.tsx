import { SERVER_URL, refreshToken } from "./constants.tsx";

const isAccessTokenExpired = async (accessToken: string): Promise<boolean> => {
  return fetch(
    `${SERVER_URL}/spotify/search?` +
      new URLSearchParams({
        query: "test",
        query_type: "track",
        access_token: accessToken,
      })
  )
    .then((response) => (response.status !== 200 ? response.json() : null))
    .then((response) => !!(response?.detail === "The access token expired"));
};

export interface RefreshAccessTokenResponse {
  accessToken: string | null;
}

export async function refreshAccessToken(
  accessToken: string
): Promise<RefreshAccessTokenResponse> {
  const url =
    `${SERVER_URL}/spotify/authorize/refresh/?` +
    new URLSearchParams({
      refresh_token: refreshToken() ?? "",
    });

  return isAccessTokenExpired(accessToken).then((isExpired: boolean) => {
    if (!isExpired) {
      return { accessToken: accessToken };
    }
    return fetch(url).then((response: Response) =>
      response.ok ? response.json() : { accessToken: null }
    );
  });
}
