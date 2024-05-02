import { SERVER_URL } from "./constants.tsx";

interface ServerResponse {
  access_token: string | null;
  refresh_token: string | null;
  expires_in: number | null;
}

const mapServerResponse = (response: ServerResponse): AuthorizeResponse => {
  return {
    accessToken: response.access_token,
    refreshToken: response.refresh_token,
    expiresIn: response.expires_in,
  };
};

export interface AuthorizeResponse {
  accessToken: string | null;
  refreshToken: string | null;
  expiresIn: number | null;
}

export function authorize(authCode: string): Promise<AuthorizeResponse> {
  return fetch(`${SERVER_URL}/spotify/authorize?authorization_code=${authCode}`)
    .then((response: Response) =>
      response.ok
        ? response.json()
        : { accessToken: null, refreshToken: null, expiresIn: null }
    )
    .then((response: ServerResponse) => mapServerResponse(response));
}
