import { SERVER_URL } from "./constants.tsx";

interface ServerResponse {
  access_token: string | null;
  refresh_token: string | null;
}

const mapServerResponse = (
  response: ServerResponse | null
): AuthorizeResponse => {
  return response
    ? {
        accessToken: response.access_token,
        refreshToken: response.refresh_token,
      }
    : { accessToken: null, refreshToken: null };
};

export interface AuthorizeResponse {
  accessToken: string | null;
  refreshToken: string | null;
}

export function authorize(authCode: string): Promise<AuthorizeResponse> {
  return fetch(`${SERVER_URL}/spotify/authorize?authorization_code=${authCode}`)
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((response: ServerResponse | null) => mapServerResponse(response));
}
