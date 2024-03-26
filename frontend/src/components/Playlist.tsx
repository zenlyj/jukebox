import React, { useEffect, useState } from "react";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { Avatar, ListItemAvatar } from "@mui/material";
import PlaylistPlayIcon from "@mui/icons-material/PlaylistPlay";
import MusicList from "./MusicList.tsx";
import { Song } from "./models/Song.tsx";
import {
  deletePlaylistSong,
  DeletePlaylistSongResponse,
} from "../api/DeletePlaylistSong.tsx";
import { getPlaylist, GetPlaylistResponse } from "../api/GetPlaylist.tsx";

interface Props {
  forceRender: () => void;
  updatePlaylistURI: (uris: string[]) => void;
  playSongs: (isPlaying: boolean) => void;
}

function Playlist(props: Props) {
  const [songs, setSongs] = useState<Song[]>([]);

  useEffect(() => {
    getPlaylistSongs();
  });

  const getPlaylistSongs = (): void => {
    getPlaylist().then((response: GetPlaylistResponse) => {
      if (response.songs.length !== songs.length) {
        setSongs(response.songs);
        props.updatePlaylistURI(response.songs.map((song) => song.uri));
      }
    });
  };

  const removePlaylistSong = (songId: number): void => {
    deletePlaylistSong(songId).then((response: DeletePlaylistSongResponse) => {
      if (response.isDeleted) {
        props.forceRender();
      } else {
        console.log("Failed to delete");
      }
    });
  };

  const listHeader = (): React.JSX.Element => {
    return (
      <ListItem disablePadding>
        <ListItemButton onClick={() => props.playSongs(true)}>
          <ListItemAvatar>
            <Avatar>
              <PlaylistPlayIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText
            primary="Playlist"
            secondary="Listen on Spotify"
            primaryTypographyProps={{ color: "#ffffff" }}
            secondaryTypographyProps={{ color: "#a1a1a1ff" }}
          />
        </ListItemButton>
      </ListItem>
    );
  };

  return (
    <MusicList
      listHeader={listHeader()}
      songs={songs}
      onClickHandler={removePlaylistSong}
    />
  );
}

export default Playlist;
