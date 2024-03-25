import React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { Divider } from "@mui/material";
import { Song } from "./models/Song";
import Box from "@mui/material/Box";

interface Props {
  songs: Song[];
  listHeader: React.JSX.Element;
  onClickHandler: (songId: string, songUri: string) => void;
}

function MusicList(props: Props) {
  const listItems = (): React.JSX.Element[] => {
    const songs = props.songs;
    let listItems: React.JSX.Element[] = [];
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

  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        bgcolor: "#141414ff",
        overflow: "auto",
        "&::-webkit-scrollbar": {
          backgroundColor: "#141414ff",
        },
        "&::-webkit-scrollbar-thumb": {
          backgroundColor: "#212224ff",
        },
      }}
    >
      <List> {listItems()} </List>
    </Box>
  )
}

export default MusicList;
