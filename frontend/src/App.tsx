import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./Home.tsx";
import SpotifyAuth from "./SpotifyAuth.tsx";
import Jukebox from "./components/Jukebox.tsx";
import Playlist from "./components/Playlist.tsx";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";
import { jbdarkgrey, jblightgrey, jbwhite } from "./utils/colors.tsx";

const theme = createTheme({
  palette: {
    background: {
      default: jbdarkgrey,
    },
  },
  typography: {
    body1: {
      color: jbwhite,
    },
    body2: {
      color: jblightgrey,
    },
    h5: {
      color: jbwhite,
    },
    h6: {
      color: jbwhite,
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/" element={<SpotifyAuth />} />
        <Route path="/home" element={<Home />}>
          <Route path="discover" element={<Jukebox />} />
          <Route path="listen" element={<Playlist />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
}

export default App;
