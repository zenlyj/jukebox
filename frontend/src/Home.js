import React, { useEffect, useState } from "react";
import SpotifyPlayer from "react-spotify-web-playback";
import { Box } from "@mui/material";
import AppHeader from "./components/AppHeader";
import Jukebox from "./components/Jukebox";
import Playlist from "./components/Playlist";
import { authorize } from "./api/api";

function Home() {
  const [playlistURI, setPlaylistURI] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [val, setVal] = useState(0);

  useEffect(() => {
    authorize();
  });

  const forceRender = () => {
    setVal(val + 1);
  };

  const updatePlaylistURI = (uris) => {
    setPlaylistURI(uris);
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
            updatePlaylistURI={updatePlaylistURI}
            forceRender={forceRender}
          />
        </Box>
      </Box>
      <Box sx={{ flex: 1 }}>
        {sessionStorage.getItem("access_token") !== null && isPlaying ? (
          <SpotifyPlayer
            token={sessionStorage.getItem("access_token")}
            uris={playlistURI}
          />
        ) : (
          <div></div>
        )}
      </Box>
    </Box>
  );
}

export default Home;
