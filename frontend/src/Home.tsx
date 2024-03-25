import React, { useEffect, useState } from "react";
import SpotifyPlayer from "react-spotify-web-playback";
import { Box } from "@mui/material";
import AppHeader from "./components/AppHeader.tsx";
import Jukebox from "./components/Jukebox.tsx";
import Playlist from "./components/Playlist.tsx";
import { authorize } from "./api/api.tsx";

function Home() {
  const [playlistURI, setPlaylistURI] = useState<string[]>([]);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [val, setVal] = useState<number>(0);

  useEffect(() => {
    authorize();
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
        {sessionStorage.getItem("access_token") !== null && isPlaying ? (
          <SpotifyPlayer
            token={sessionStorage.getItem("access_token") ?? ""}
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
