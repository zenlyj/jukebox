import { SERVER_URL } from "./constants.tsx";

export interface GetUserProfileResponse {
  name: string | null;
  userId: string | null;
}

export interface ServerResponse {
  name: string;
  user_id: string;
}

const mapServerResponse = (
  response: ServerResponse | null
): GetUserProfileResponse => {
  if (!response) {
    return {
      name: null,
      userId: null,
    };
  }
  return {
    name: response.name,
    userId: response.user_id,
  };
};

export async function getUserProfile(
  accessToken: string
): Promise<GetUserProfileResponse> {
  return fetch(`${SERVER_URL}/spotify/user-profile/`, {
    headers: {
      Authorization: accessToken,
    },
  })
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((response: ServerResponse | null) => mapServerResponse(response));
}
