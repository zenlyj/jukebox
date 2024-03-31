import React, { useEffect } from "react";

function SpotifyAuth() {
  useEffect(() => {
    const SPOTIFY_CLIENT_ID = process.env.REACT_APP_CLIENT_ID;
    const CLIENT_URL = process.env.REACT_APP_CLIENT_URL;
    const redirectUri = `${CLIENT_URL}/home/discover`;
    window.location.replace(
      `https://accounts.spotify.com/authorize?response_type=code&client_id=${SPOTIFY_CLIENT_ID}&redirect_uri=${redirectUri}&scope=streaming,user-read-email,user-read-private,user-read-playback-state,user-modify-playback-state`
    );
  });

  return <div> Loading... </div>;
}

export default SpotifyAuth;
