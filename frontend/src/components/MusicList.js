import React, { useEffect, useState } from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { Divider } from "@mui/material";

function MusicList(props) {
  const listItems = () => {
    const songs = props.songs;
    let listItems = [];
    listItems.push(props.listHeader);

    if (songs.length === 0) {
      listItems.push(
        <ListItem>
          <ListItemText
            primary="No Songs Yet..."
            primaryTypographyProps={{ color: "#a1a1a1ff" }}
          />
        </ListItem>
      );
      return listItems;
    }

    for (let i = 0; i < songs.length; i++) {
      const song = songs[i];
      const listItem = (
        <ListItem disablePadding key={song.id}>
          <ListItemButton
            onClick={() => props.onClickHandler(song.id, song.uri)}
          >
            <ListItemText
              primary={song.title}
              secondary={song.artist}
              primaryTypographyProps={{ color: "#ffffff" }}
              secondaryTypographyProps={{ color: "#a1a1a1ff" }}
            />
          </ListItemButton>
        </ListItem>
      );
      listItems.push(listItem);
      listItems.push(<Divider sx={{ bgcolor: "#212224ff" }} />);
    }
    return listItems;
  };

  return <List> {listItems()} </List>;
}

export default MusicList;
