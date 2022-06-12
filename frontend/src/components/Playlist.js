import React, { useEffect, useState } from "react";
import ListContainer from "./ListContainer";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { deletePlaylistSong, getPlaylist } from "../api/api";
import { Avatar, ListItemAvatar } from "@mui/material";
import PlaylistPlayIcon from "@mui/icons-material/PlaylistPlay";

function Playlist(props) {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    getPlaylistSongs();
  });

  const getPlaylistSongs = () => {
    getPlaylist().then((value) =>
      Promise.resolve(value.json()).then((playlistSongs) => {
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

  const removePlaylistSong = (songId) => {
    deletePlaylistSong(songId).then((response) => {
      if (response.status == 200) {
        props.forceRender();
      } else {
        console.log("Failed to delete");
      }
    });
  };

  const listHeader = () => {
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
    <ListContainer
      listHeader={listHeader()}
      songs={songs}
      onClickHandler={removePlaylistSong}
    />
  );
}

export default Playlist;
