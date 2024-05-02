import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import { CircularProgress } from "@mui/material";
import AppHeader from "./components/AppHeader.tsx";
import { authorize, AuthorizeResponse } from "./api/Authorize.tsx";
import {
  accessToken,
  authCode,
  expiresIn,
  expireTime,
} from "./api/constants.tsx";
import {
  refreshAccessToken,
  RefreshAccessTokenResponse,
} from "./api/RefreshAccessToken.tsx";
import { Outlet } from "react-router-dom";
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
        if (
          response.accessToken &&
          response.refreshToken &&
          response.expiresIn
        ) {
          sessionStorage.setItem("accessToken", response.accessToken);
          sessionStorage.setItem("refreshToken", response.refreshToken);
          sessionStorage.setItem("expiresIn", response.expiresIn?.toString());
          sessionStorage.setItem("expireTime", getExpireTime().toString());
          setIsLoggedIn(true);
        } else {
          setIsLoggedIn(false);
        }
      });
    }
  }, []);

  useEffect(() => {
    if (!isAccessTokenExpired()) {
      setIsLoggedIn(true);
      return;
    }
    const token = accessToken();
    if (token) {
      refreshAccessToken(token).then((response: RefreshAccessTokenResponse) => {
        if (response.accessToken) {
          sessionStorage.setItem("accessToken", response.accessToken);
          sessionStorage.setItem("expireTime", getExpireTime().toString());
          setIsLoggedIn(true);
        } else {
          console.log("Unable to refresh access token");
          setIsLoggedIn(false);
        }
      });
    }
  });

  useEffect(() => {
    getPlaylistSize().then((response: GetPlaylistSizeResponse) => {
      setPlaylistSize(response.size);
    });
  }, [isLoggedIn]);

  const isAccessTokenExpired = (): boolean => {
    const currTime = new Date().getTime() / 1000;
    return currTime >= (expireTime() ?? 0);
  };

  const getExpireTime = (): number => {
    const duration = expiresIn() ?? 0;
    return new Date().getTime() / 1000 + duration;
  };

  const isDiscover = (): boolean => {
    return mode === Mode.DISCOVER;
  };

  const isListen = (): boolean => {
    return mode === Mode.LISTEN;
  };

  const containerStyle = (flexDirection: "row" | "column") => ({
    display: "flex",
    flexDirection: flexDirection,
    height: "100vh",
  });

  return isLoggedIn ? (
    <Box sx={containerStyle("column")}>
      <Box sx={{ height: "7%" }}>
        <AppHeader
          playlistSize={playlistSize}
          currMode={mode}
          setGenre={setGenre}
          setMode={setMode}
        />
      </Box>
      <Box
        sx={{
          flex: 1,
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
