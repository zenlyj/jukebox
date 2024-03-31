import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import AppHeader from "./components/AppHeader.tsx";
import { authorize, AuthorizeResponse } from "./api/Authorize.tsx";
import { accessToken, authCode } from "./api/constants.tsx";
import {
  refreshAccessToken,
  RefreshAccessTokenResponse,
} from "./api/RefreshAccessToken.tsx";
import { Outlet } from "react-router-dom";

function Home() {
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
      <Box sx={{ flex: 9, height: "85vh" }}>
        <Outlet />
      </Box>
    </Box>
  );
}

export default Home;
