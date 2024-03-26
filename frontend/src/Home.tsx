import React, { useEffect, useState } from "react";
import SpotifyPlayer from "react-spotify-web-playback";
import { Box } from "@mui/material";
import AppHeader from "./components/AppHeader.tsx";
import Jukebox from "./components/Jukebox.tsx";
import Playlist from "./components/Playlist.tsx";
import { authorize, AuthorizeResponse } from "./api/Authorize.tsx";
import { accessToken, authCode } from "./api/constants.tsx";
import {
  refreshAccessToken,
  RefreshAccessTokenResponse,
} from "./api/RefreshAccessToken.tsx";

function Home() {
  const [playlistURI, setPlaylistURI] = useState<string[]>([]);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [val, setVal] = useState<number>(0);

  useEffect(() => {
    const code = authCode();
    const token = accessToken();
    if (!token && code) {
      authorize(code).then((response: AuthorizeResponse) => {
        if (response.accessToken && response.refreshToken) {
          sessionStorage.setItem("accessToken", response.accessToken);
          sessionStorage.setItem("refreshToken", response.refreshToken);
        }
      });
    } else if (token) {
      refreshAccessToken(token).then((response: RefreshAccessTokenResponse) => {
        if (response.accessToken) {
          sessionStorage.setItem("accessToken", response.accessToken);
        } else {
          console.log("Unable to refresh access token");
        }
      });
    }
  });

  const forceRender = (): void => {
    setVal(val + 1);
  };

  return (
    <Box
      sx={{
        bgcolor: "#141414ff",
        display: "flex",
        flexDirection: "column",
        height: "100vh",
      }}
    >
      <Box sx={{ flex: 1 }}>
        <AppHeader />
      </Box>
      <Box
        sx={{ flex: 8, display: "flex", flexDirection: "row", height: "85vh" }}
      >
        <Box sx={{ flex: 1 }}>
          <Jukebox forceRender={forceRender} />
        </Box>
        <Box sx={{ flex: 1 }}>
          <Playlist
            playSongs={setIsPlaying}
            updatePlaylistURI={setPlaylistURI}
            forceRender={forceRender}
          />
        </Box>
      </Box>
      <Box sx={{ flex: 1 }}>
        {accessToken() && isPlaying ? (
          <SpotifyPlayer token={accessToken() ?? ""} uris={playlistURI} />
        ) : (
          <div></div>
        )}
      </Box>
    </Box>
  );
}

export default Home;
