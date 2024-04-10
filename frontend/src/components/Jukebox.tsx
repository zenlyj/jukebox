import React, { useEffect, useState } from "react";
import MusicList from "./MusicList.tsx";
import { MusicListPagination } from "./MusicListPagination.tsx";
import { Song } from "./models/Song.tsx";
import { getSongs, GetSongsResponse } from "../api/GetSongs.tsx";
import {
  addSongToPlaylist,
  AddSongToPlaylistResponse,
} from "../api/AddSongToPlaylist.tsx";
import { useOutletContext } from "react-router-dom";
import { HomeContext } from "./models/HomeContext.tsx";
import { Box } from "@mui/material";

function Jukebox() {
  const [songs, setSongs] = useState<Song[]>([]);
  const [songCount, setSongCount] = useState<number>(0);
  const { playlistSize, setPlaylistSize, genre } =
    useOutletContext<HomeContext>();
  const pageSize = 10;

  useEffect(() => {
    if (songs.length === 0) {
      getSongs(genre, 1, pageSize).then((response: GetSongsResponse) => {
        if (response.songs.length !== 0) {
          setSongs(response.songs);
          setSongCount(response.songCount);
        }
      });
    }
  });

  const addToPlaylist = (songId: number): void => {
    addSongToPlaylist(songId).then((response: AddSongToPlaylistResponse) => {
      if (response.isAdded) {
        console.log("Successfully added to playlist");
        setPlaylistSize(playlistSize + 1);
      } else {
        console.log("Failed to add to playlist");
      }
    });
  };

  const handlePageChange = (event, pageNumber: number): void => {
    getSongs(genre, pageNumber, pageSize).then((response: GetSongsResponse) => {
      if (response.songs.length !== 0) {
        setSongs(response.songs);
        setSongCount(response.songCount);
      }
    });
  };

  const getPageCount = () => {
    return Math.ceil(songCount / pageSize);
  };

  return (
    <Box sx={{ padding: "1rem" }}>
      <MusicList songs={songs} onClickHandler={addToPlaylist} />
      <Box sx={{ marginTop: "1rem" }}>
        <MusicListPagination
          pageCount={getPageCount()}
          handlePageChange={handlePageChange}
        />
      </Box>
    </Box>
  );
}

export default Jukebox;
