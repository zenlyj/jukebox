import React, { useEffect, useState } from "react";
import MusicList from "./MusicList.tsx";
import { Song } from "./models/Song.tsx";
import { getSongs, GetSongsResponse } from "../api/GetSongs.tsx";
import {
  addSongToPlaylist,
  AddSongToPlaylistResponse,
} from "../api/AddSongToPlaylist.tsx";
import { useOutletContext } from "react-router-dom";
import { PlaylistSizeContext } from "./models/PlaylistSizeContext.tsx";
import { Genre } from "./models/Genre.tsx";

function Jukebox() {
  const [genre, setGenre] = useState<Genre>(Genre.HIPHOP);
  const [songs, setSongs] = useState<Song[]>([]);
  const { playlistSize, setPlaylistSize } =
    useOutletContext<PlaylistSizeContext>();

  useEffect(() => {
    if (songs.length === 0) {
      getSongs(genre).then((response: GetSongsResponse) => {
        setSongs(response.songs);
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

  return <MusicList songs={songs} onClickHandler={addToPlaylist} />;
}

export default Jukebox;
