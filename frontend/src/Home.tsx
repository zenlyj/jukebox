import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import { CircularProgress } from "@mui/material";
import AppHeader from "./components/AppHeader.tsx";
import { authorize, AuthorizeResponse } from "./api/Authorize.tsx";
import { authCode } from "./api/constants.tsx";
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
import {
  getAccessToken,
  getRefreshToken,
  getTokenExpireTime,
  getTokenExpiresIn,
  getUserInfo,
  setAccessToken,
  setRefreshToken,
  setTokenExpireTime,
  setTokenExpiresIn,
  setUserInfo,
} from "./utils/session.tsx";
import {
  GetUserProfileResponse,
  getUserProfile,
} from "./api/GetUserProfile.tsx";

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState<Boolean>(false);
  const [playlistSize, setPlaylistSize] = useState<number>(0);
  const [genre, setGenre] = useState<Genre | null>(null);
  const [mode, setMode] = useState<Mode>(Mode.DISCOVER);

  useEffect(() => {
    const code = authCode();
    if (getAccessToken() || !code) {
      return;
    }
    authorize(code)
      .then((response: AuthorizeResponse) => {
        if (
          !response.accessToken ||
          !response.refreshToken ||
          !response.expiresIn
        ) {
          setIsLoggedIn(false);
          return null;
        }
        setAccessToken(response.accessToken);
        setRefreshToken(response.refreshToken);
        setTokenExpiresIn(response.expiresIn);
        setTokenExpireTime(Date.now() + getTokenExpiresIn() * 1000);
        return getUserProfile(response.accessToken);
      })
      .then((response: GetUserProfileResponse | null) => {
        if (!response) {
          return null;
        }
        setUserInfo(response.name, response.userId);
        setIsLoggedIn(true);
      });
  }, []);

  useEffect(() => {
    if (Date.now() < getTokenExpireTime()) {
      setIsLoggedIn(true);
      return;
    }
    const accessToken = getAccessToken();
    const refreshToken = getRefreshToken();
    if (!accessToken || !refreshToken) {
      return;
    }
    refreshAccessToken(accessToken, refreshToken).then(
      (response: RefreshAccessTokenResponse) => {
        if (!response.accessToken) {
          console.log("Unable to refresh access token");
          setIsLoggedIn(false);
          return;
        }
        setAccessToken(response.accessToken);
        setTokenExpiresIn(response.expiresIn);
        setTokenExpireTime(Date.now() + getTokenExpiresIn() * 1000);
        setIsLoggedIn(true);
      }
    );
  });

  useEffect(() => {
    if (mode) {
      return;
    }

    const url = new URL(window.location.href);
    const names = url.pathname.split("/");
    if (names.some((name) => name === Mode.DISCOVER)) {
      setMode(Mode.DISCOVER);
    }
    if (names.some((name) => name === Mode.LISTEN)) {
      setMode(Mode.LISTEN);
    }
  });

  useEffect(() => {
    const spotifyUserId = getUserInfo()?.userId;
    if (!spotifyUserId) {
      return;
    }
    getPlaylistSize(spotifyUserId).then((response: GetPlaylistSizeResponse) => {
      setPlaylistSize(response.size);
    });
  }, [isLoggedIn]);

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
