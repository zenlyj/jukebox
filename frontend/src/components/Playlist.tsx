import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import MusicList from "./MusicList.tsx";
import { Song } from "./models/Song.tsx";
import {
  deletePlaylistSong,
  DeletePlaylistSongResponse,
} from "../api/DeletePlaylistSong.tsx";
import { getPlaylist, GetPlaylistResponse } from "../api/GetPlaylist.tsx";
import SpotifyPlayer from "react-spotify-web-playback";
import { accessToken } from "../api/constants.tsx";
import { useOutletContext } from "react-router-dom";
import { HomeContext } from "./models/HomeContext.tsx";

function Playlist() {
  const [songs, setSongs] = useState<Song[]>([]);
  const [uris, setUris] = useState<string[]>([]);
  const { setPlaylistSize } = useOutletContext<HomeContext>();

  useEffect(() => {
    getPlaylistSongs();
  });

  const getPlaylistSongs = (): void => {
    getPlaylist().then((response: GetPlaylistResponse) => {
      if (response.songs.length !== songs.length) {
        setSongs(response.songs);
        setUris(response.songs.map((song) => song.uri));
        setPlaylistSize(response.songs.length);
      }
    });
  };

  const removePlaylistSong = (songId: number): void => {
    deletePlaylistSong(songId).then((response: DeletePlaylistSongResponse) => {
      if (response.isDeleted) {
        console.log("Successfully removed song from playlist");
        getPlaylistSongs();
      } else {
        console.log("Failed to delete");
      }
    });
  };

  return (
    <Box sx={{ height: "100%" }}>
      <Box sx={{ height: "85%" }}>
        <MusicList songs={songs} onClickHandler={removePlaylistSong} />
      </Box>
      <Box
        sx={{
          height: "15%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-end",
        }}
      >
        <SpotifyPlayer token={accessToken() ?? ""} uris={uris} />
      </Box>
    </Box>
  );
}

export default Playlist;
