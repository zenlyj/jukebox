import React, { useEffect, useState } from "react";
import ListContainer from "./ListContainer";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { getSongs, addSongToPlaylist } from "../api/api";
import { Avatar, ListItemAvatar } from "@mui/material";
import PlaylistAddIcon from "@mui/icons-material/PlaylistAdd";

function Jukebox(props) {
  const modes = ["Latest", "All"];

  const [mode, setMode] = useState(0);
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    if (songs.length === 0) {
      getSongs().then((value) =>
        Promise.resolve(value.json()).then((value) => setSongs(value))
      );
    }
  });

  const addToPlaylist = (songId) => {
    addSongToPlaylist(songId).then((response) => {
      if (response.status == 200) {
        props.forceRender();
      } else {
        console.log("Failed to add to playlist");
      }
    });
  };

  const changeMode = () => {
    const newMode = (mode + 1) % modes.length;
    setMode(newMode);
  };

  const listHeader = () => {
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
    <ListContainer
      listHeader={listHeader()}
      songs={songs}
      onClickHandler={addToPlaylist}
    />
  );
}

export default Jukebox;
