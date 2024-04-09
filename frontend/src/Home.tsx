import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
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
import { GenreSelection } from "./components/GenreSelection.tsx";
import { Genre } from "./components/models/Genre.tsx";
import { Mode } from "./components/models/Mode.tsx";
import {
  GetPlaylistSizeResponse,
  getPlaylistSize,
} from "./api/GetPlaylistSize.tsx";

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState<Boolean>(false);
  const [playlistSize, setPlaylistSize] = useState<number>(0);
  const [genre, setGenre] = useState<Genre | null>(null);
  const [mode, setMode] = useState<Mode>(Mode.DISCOVER);

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
      getPlaylistSize().then((response: GetPlaylistSizeResponse) => {
        if (response.size !== playlistSize) {
          setPlaylistSize(response.size);
        }
      });
    }
  });

  const isDiscover = (): boolean => {
    return mode === Mode.DISCOVER;
  };

  const isListen = (): boolean => {
    return mode === Mode.LISTEN;
  };

  const containerStyle = (flexDirection: "row" | "column") => ({
    bgcolor: "#141414ff",
    display: "flex",
    flexDirection: flexDirection,
    height: "100vh",
  });

  return isLoggedIn ? (
    <Box sx={containerStyle("column")}>
      <Box sx={{ flex: 1 }}>
        <AppHeader
          playlistSize={playlistSize}
          setGenre={setGenre}
          setMode={setMode}
        />
      </Box>
      <Box
        sx={{
          flex: 12,
          overflow: "auto",
        }}
      >
        {(isDiscover() && genre) || isListen() ? (
          <Outlet
            context={{
              playlistSize: playlistSize,
              setPlaylistSize: setPlaylistSize,
              genre: genre,
            }}
          />
        ) : (
          <Box
            sx={{
              height: "100%",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
            }}
          >
            <GenreSelection setGenre={setGenre} />
          </Box>
        )}
      </Box>
    </Box>
  ) : (
    <Box sx={{ ...containerStyle("row"), justifyContent: "center" }}>
      <CircularProgress />
    </Box>
  );
}

export default Home;
