import React, { useEffect } from "react";

function SpotifyAuth(props) {
  useEffect(() => {
    const SPOTIFY_CLIENT_ID = process.env.REACT_APP_CLIENT_ID;
    const CLIENT_URL = process.env.REACT_APP_CLIENT_URL;
    window.location.replace(
      `https://accounts.spotify.com/authorize?response_type=code&client_id=${SPOTIFY_CLIENT_ID}&redirect_uri=${CLIENT_URL}/home/&scope=streaming,user-read-email,user-read-private,user-read-playback-state,user-modify-playback-state`
    );
  });

  return <div> Loading... </div>;
}

export default SpotifyAuth;
