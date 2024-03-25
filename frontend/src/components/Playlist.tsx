import React, { useEffect, useState } from "react";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { deletePlaylistSong, getPlaylist } from "../api/api.tsx";
import { Avatar, ListItemAvatar } from "@mui/material";
import PlaylistPlayIcon from "@mui/icons-material/PlaylistPlay";
import MusicList from "./MusicList.tsx";
import { Song } from "./models/Song.tsx";

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
    getPlaylist().then((value) =>
      Promise.resolve(value?.json()).then((playlistSongs: Song[]) => {
        if (
          playlistSongs !== undefined &&
          playlistSongs.length !== songs.length
        ) {
          setSongs(playlistSongs);
          props.updatePlaylistURI(playlistSongs.map((song) => song.uri));
        }
      })
    );
  };

  const removePlaylistSong = (songId: string): void => {
    deletePlaylistSong(songId).then((response) => {
      if (response?.status == 200) {
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
