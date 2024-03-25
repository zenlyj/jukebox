const SERVER_URL = process.env.REACT_APP_SERVER_URL;
const accessToken = (): string | null => sessionStorage.getItem("access_token");
const refreshToken = (): string | null => sessionStorage.getItem("refresh_token");

async function authorize(): Promise<void> {
  const windowURL = window.location.search;
  const params = new URLSearchParams(windowURL);
  const authCode = params.get("code");
  const token = accessToken()

  if (token !== null) {
    accessTokenExpiryCheck(token);
  }
  if (token === null && authCode !== null) {
    return fetch(
      `${SERVER_URL}/spotify/authorize?authorization_code=${authCode}`
    ).then((value) =>
      Promise.resolve(value.json()).then((value) => {
        sessionStorage.setItem("access_token", value.access_token);
        sessionStorage.setItem("refresh_token", value.refresh_token);
      })
    );
  }
}

const accessTokenExpiryCheck = async (accessToken: string): Promise<void> => {
  fetch(
    `${SERVER_URL}/spotify/search?` +
      new URLSearchParams({
        query: "test",
        query_type: "track",
        access_token: accessToken,
      })
  ).then((response) => {
    if (response.status === 200) return;
    response.json().then((response) => {
      if (response.detail === "The access token expired") {
        refreshAccessToken();
      }
    });
  });
};

const refreshAccessToken = async (): Promise<void> => {
  const url =
    `${SERVER_URL}/spotify/authorize/refresh/?` +
    new URLSearchParams({
      refresh_token: refreshToken() ?? "",
    });

  fetch(url).then((response) => {
    if (response.status !== 200) {
      console.log("Unable to refresh access token");
      return;
    }
    response.json().then((response) => {
      sessionStorage.setItem("access_token", response.access_token);
      console.log("Access Token refreshed");
    });
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

async function deletePlaylistSong(songId: string): Promise<Response | undefined> {
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
