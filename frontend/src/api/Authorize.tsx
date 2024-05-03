import { SERVER_URL } from "./constants.tsx";

interface ServerResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

const mapServerResponse = (
  response: ServerResponse | null
): AuthorizeResponse =>
  !response
    ? { accessToken: null, refreshToken: null, expiresIn: null }
    : {
        accessToken: response.access_token,
        refreshToken: response.refresh_token,
        expiresIn: response.expires_in,
      };

export interface AuthorizeResponse {
  accessToken: string | null;
  refreshToken: string | null;
  expiresIn: number | null;
}

export function authorize(authCode: string): Promise<AuthorizeResponse> {
  return fetch(`${SERVER_URL}/spotify/authorize?authorization_code=${authCode}`)
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((response: ServerResponse | null) => mapServerResponse(response));
}
