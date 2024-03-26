import { SERVER_URL } from "./constants.tsx";

export interface AuthorizeResponse {
  accessToken: string | null;
  refreshToken: string | null;
}

export function authorize(authCode: string): Promise<AuthorizeResponse> {
  return fetch(
    `${SERVER_URL}/spotify/authorize?authorization_code=${authCode}`
  ).then((response: Response) =>
    response.ok ? response.json() : { accessToken: null, refreshToken: null }
  );
}
