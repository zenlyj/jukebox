const SERVER_URL = process.env.REACT_APP_SERVER_URL;
const accessToken = (): string | null => sessionStorage.getItem("access_token");
const refreshToken = (): string | null =>
  sessionStorage.getItem("refresh_token");

function authorize(): void {
  const windowURL = window.location.search;
  const params = new URLSearchParams(windowURL);
  const authCode = params.get("code");
  const token = accessToken();

  if (token !== null) {
    isAccessTokenExpired(token).then((isExpired) => {
      if (isExpired) {
        refreshAccessToken();
      }
    });
  }
  if (token === null && authCode !== null) {
    fetch(`${SERVER_URL}/spotify/authorize?authorization_code=${authCode}`)
      .then((value) => value.json())
      .then((value) => {
        sessionStorage.setItem("access_token", value.access_token);
        sessionStorage.setItem("refresh_token", value.refresh_token);
      });
  }
}

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

const refreshAccessToken = (): void => {
  const url =
    `${SERVER_URL}/spotify/authorize/refresh/?` +
    new URLSearchParams({
      refresh_token: refreshToken() ?? "",
    });

  fetch(url)
    .then((response) => {
      if (response.status !== 200) {
        console.log("Unable to refresh access token");
        return null;
      } else {
        return response.json();
      }
    })
    .then((response) => {
      if (response) {
        sessionStorage.setItem("access_token", response.access_token);
        console.log("Access Token refreshed");
      }
    });
};

async function getSongs(): Promise<Response> {
  return fetch(`${SERVER_URL}/songs/`);
}

async function addSongToPlaylist(songId: string): Promise<Response> {
  return fetch(`${SERVER_URL}/playlist/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session: accessToken(),
      song: songId,
    }),
  });
}

async function getPlaylist(): Promise<Response | undefined> {
  if (accessToken() !== null) {
    return fetch(`${SERVER_URL}/playlist/?session=${accessToken()}`);
  }
}

async function deletePlaylistSong(
  songId: string
): Promise<Response | undefined> {
  if (accessToken() !== null) {
    return fetch(
      `${SERVER_URL}/playlist/?session=${accessToken()}&song_id=${songId}`,
      { method: "DELETE" }
    );
  }
}

export {
  getSongs,
  addSongToPlaylist,
  getPlaylist,
  deletePlaylistSong,
  authorize,
};
