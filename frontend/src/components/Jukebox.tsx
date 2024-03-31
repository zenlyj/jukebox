import React, { useEffect, useState } from "react";
import MusicList from "./MusicList.tsx";
import { Song } from "./models/Song.tsx";
import { getSongs, GetSongsResponse } from "../api/GetSongs.tsx";
import {
  addSongToPlaylist,
  AddSongToPlaylistResponse,
} from "../api/AddSongToPlaylist.tsx";

function Jukebox() {
  const [songs, setSongs] = useState<Song[]>([]);

  useEffect(() => {
    if (songs.length === 0) {
      getSongs().then((response: GetSongsResponse) => {
        setSongs(response.songs);
      });
    }
  });

  const addToPlaylist = (songId: number): void => {
    addSongToPlaylist(songId).then((response: AddSongToPlaylistResponse) => {
      if (response.isAdded) {
        console.log("Successfully added to playlist");
      } else {
        console.log("Failed to add to playlist");
      }
    });
  };

  return <MusicList songs={songs} onClickHandler={addToPlaylist} />;
}

export default Jukebox;
