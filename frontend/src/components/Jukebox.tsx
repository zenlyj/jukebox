import React, { useEffect, useState } from "react";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { Avatar, ListItemAvatar } from "@mui/material";
import PlaylistAddIcon from "@mui/icons-material/PlaylistAdd";
import MusicList from "./MusicList.tsx";
import { Song } from "./models/Song.tsx";
import { getSongs, GetSongsResponse } from "../api/GetSongs.tsx";
import {
  addSongToPlaylist,
  AddSongToPlaylistResponse,
} from "../api/AddSongToPlaylist.tsx";

interface Props {
  forceRender: () => void;
}

function Jukebox(props: Props) {
  const modes = ["Latest", "All"];

  const [mode, setMode] = useState<number>(0);
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
        props.forceRender();
      } else {
        console.log("Failed to add to playlist");
      }
    });
  };

  const changeMode = (): void => {
    const newMode = (mode + 1) % modes.length;
    setMode(newMode);
  };

  const listHeader = (): React.JSX.Element => {
    return (
      <ListItem disablePadding>
        <ListItemButton onClick={() => changeMode()}>
          <ListItemAvatar>
            <Avatar>
              <PlaylistAddIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText
            primary="Song Selection"
            secondary={modes[mode]}
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
      onClickHandler={addToPlaylist}
    />
  );
}

export default Jukebox;
