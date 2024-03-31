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

function Playlist() {
  const [songs, setSongs] = useState<Song[]>([]);
  const [uris, setUris] = useState<string[]>([]);

  useEffect(() => {
    getPlaylistSongs();
  });

  const getPlaylistSongs = (): void => {
    getPlaylist().then((response: GetPlaylistResponse) => {
      if (response.songs.length !== songs.length) {
        setSongs(response.songs);
        setUris(response.songs.map((song) => song.uri));
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
    <Box>
      <MusicList songs={songs} onClickHandler={removePlaylistSong} />
      <SpotifyPlayer token={accessToken() ?? ""} uris={uris} />
    </Box>
  );
}

export default Playlist;
