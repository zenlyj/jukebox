import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import { CircularProgress } from "@mui/material";
import AppHeader from "./components/AppHeader.tsx";
import { authorize, AuthorizeResponse } from "./api/Authorize.tsx";
import { accessToken, authCode } from "./api/constants.tsx";
import {
  refreshAccessToken,
  RefreshAccessTokenResponse,
} from "./api/RefreshAccessToken.tsx";
import { Outlet } from "react-router-dom";
import { GetPlaylistResponse, getPlaylist } from "./api/GetPlaylist.tsx";

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState<Boolean>(false);
  const [playlistSize, setPlaylistSize] = useState<number>(0);

  useEffect(() => {
    const code = authCode();
    const token = accessToken();
    if (!token && code) {
      authorize(code).then((response: AuthorizeResponse) => {
        if (response.accessToken && response.refreshToken) {
          sessionStorage.setItem("accessToken", response.accessToken);
          sessionStorage.setItem("refreshToken", response.refreshToken);
          setIsLoggedIn(true);
        } else {
          setIsLoggedIn(false);
        }
      });
    } else if (token) {
      refreshAccessToken(token).then((response: RefreshAccessTokenResponse) => {
        if (response.accessToken) {
          sessionStorage.setItem("accessToken", response.accessToken);
          setIsLoggedIn(true);
        } else {
          console.log("Unable to refresh access token");
          setIsLoggedIn(false);
        }
      });
    }
    if (isLoggedIn && playlistSize === 0) {
      getPlaylist().then((response: GetPlaylistResponse) => {
        if (response.songs.length !== playlistSize) {
          setPlaylistSize(response.songs.length);
        }
      });
    }
  });

  const containerStyle = (flexDirection: "row" | "column") => ({
    bgcolor: "#141414ff",
    display: "flex",
    flexDirection: flexDirection,
    height: "100vh",
  });

  return isLoggedIn ? (
    <Box sx={containerStyle("column")}>
      <Box sx={{ flex: 1 }}>
        <AppHeader playlistSize={playlistSize} />
      </Box>
      <Box sx={{ flex: 9, overflow: "auto" }}>
        <Outlet
          context={{
            playlistSize: playlistSize,
            setPlaylistSize: setPlaylistSize,
          }}
        />
      </Box>
    </Box>
  ) : (
    <Box sx={{ ...containerStyle("row"), justifyContent: "center" }}>
      <CircularProgress />
    </Box>
  );
}

export default Home;
