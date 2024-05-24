import { SERVER_URL } from "./constants.tsx";

export interface AddUserPreferenceResponse {
  spotifyUserId: string | null;
  artistGenreIds: number[];
  message: string;
}

export interface ServerResponse {
  spotify_user_id: string;
  artist_genre_ids: number[];
  message: string;
}

const mapServerResponse = (
  response: ServerResponse | null
): AddUserPreferenceResponse => {
  if (!response) {
    return {
      spotifyUserId: null,
      artistGenreIds: [],
      message: "Failed to add user preference!",
    };
  }
  return {
    spotifyUserId: response.spotify_user_id,
    artistGenreIds: response.artist_genre_ids,
    message: response.message,
  };
};

export async function addUserPreference(
  spotifyUserId: string,
  songId: number
): Promise<AddUserPreferenceResponse> {
  return fetch(`${SERVER_URL}/preference/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      spotify_user_id: spotifyUserId,
      song_id: songId,
    }),
  })
    .then((response: Response) => (response.ok ? response.json() : null))
    .then((response: ServerResponse | null) => mapServerResponse(response));
}
