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
  const [pageNum, setPageNum] = useState<number>(1);
  const { playlistSize, setPlaylistSize, genre } =
    useOutletContext<HomeContext>();
  const pageSize = 10;

  useEffect(() => {
    getRecommendedSongs(pageNum);
  }, [pageNum]);

  const getRecommendedSongs = (pageNum: number) => {
    getSongs(genre, pageNum, pageSize).then((response: GetSongsResponse) => {
      setSongs(response.songs);
      setSongCount(response.songCount);
    });
  };

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
    setPageNum(pageNumber);
  };

  const getPageCount = (): number => {
    return Math.ceil(songCount / pageSize);
  };

  return (
    <Box
      sx={{
        padding: "1rem",
        display: "flex",
        flexDirection: "column",
        height: "100%",
        justifyContent: "space-between",
      }}
    >
      <MusicList
        songs={songs}
        displayDate={true}
        onClickHandler={addToPlaylist}
      />
      <MusicListPagination
        pageCount={getPageCount()}
        pageNum={pageNum}
        handlePageChange={handlePageChange}
      />
    </Box>
  );
}

export default Jukebox;
