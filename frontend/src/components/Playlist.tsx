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
import { MusicListPagination } from "./MusicListPagination.tsx";

function Playlist() {
  const [songs, setSongs] = useState<Song[]>([]);
  const [uris, setUris] = useState<string[]>([]);
  const [songCount, setSongCount] = useState<number>(0);
  const { setPlaylistSize } = useOutletContext<HomeContext>();
  const pageSize = 10;

  useEffect(() => {
    if (songs.length === 0) {
      getPlaylistSongs();
    }
  });

  const isSongChanged = (newSongs: Song[]): boolean => {
    const currIds = new Set(songs.map((song) => song.id));
    return songCount > pageSize
      ? newSongs.some((song) => !currIds.has(song.id))
      : newSongs.length !== songs.length;
  };

  const getPlaylistSongs = (): void => {
    getPlaylist(1, pageSize).then((response: GetPlaylistResponse) => {
      if (isSongChanged(response.songs)) {
        setSongs(response.songs);
        setUris(response.songs.map((song) => song.uri));
        setSongCount(response.playlistSize);
        setPlaylistSize(response.playlistSize);
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

  const handlePageChange = (event, pageNumber: number): void => {
    getPlaylist(pageNumber, pageSize).then((response: GetPlaylistResponse) => {
      if (response.songs.length !== 0) {
        setSongs(response.songs);
        setUris(response.songs.map((song) => song.uri));
        setSongCount(response.playlistSize);
        setPlaylistSize(response.playlistSize);
      }
    });
  };

  const getPageCount = () => {
    return Math.ceil(songCount / pageSize);
  };

  return (
    <Box sx={{ height: "100%" }}>
      <Box sx={{ height: "85%" }}>
        <MusicList songs={songs} onClickHandler={removePlaylistSong} />
        <MusicListPagination
          pageCount={getPageCount()}
          handlePageChange={handlePageChange}
        />
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
