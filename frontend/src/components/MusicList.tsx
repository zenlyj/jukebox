import React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { Divider } from "@mui/material";
import { Song } from "./models/Song";
import Box from "@mui/material/Box";
import { ListItemAvatar } from "@mui/material";
import LinearProgress from "@mui/material/LinearProgress";

const formatArtistNames = (artistNames: string[]): string => {
  return artistNames.join(", ");
};

const formatDuration = (duration: number): string => {
  const totalSeconds = duration / 1000;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = Math.floor(totalSeconds - minutes * 60);
  const formatSeconds = seconds < 10 ? `0${seconds}` : seconds;
  return `${minutes}:${formatSeconds}`;
};

interface Props {
  songs: Song[];
  onClickHandler: (songId: number, songUri: string) => void;
}

function MusicList(props: Props) {
  const listItems = (): React.JSX.Element[] => {
    const songs = props.songs;
    const listItems: React.JSX.Element[] = [];

    songs.forEach((song) => {
      const listItem = (
        <ListItem disablePadding key={song.id}>
          <ListItemButton
            onClick={() => props.onClickHandler(song.id, song.uri)}
            sx={{
              ":hover": {
                opacity: 0.5,
              },
            }}
          >
            <ListItemAvatar sx={{ paddingRight: "1rem" }}>
              <img src={song.albumCover} width={50} height={50}></img>
            </ListItemAvatar>
            <ListItemText
              primary={song.name}
              secondary={formatArtistNames(song.artistNames)}
              primaryTypographyProps={{ color: "#ffffff" }}
              secondaryTypographyProps={{ color: "#a1a1a1ff" }}
            />
            <ListItemText
              secondary={formatDuration(song.duration)}
              secondaryTypographyProps={{
                color: "#a1a1a1ff",
                textAlign: "right",
              }}
            />
          </ListItemButton>
        </ListItem>
      );
      listItems.push(listItem);
      listItems.push(<Divider sx={{ bgcolor: "#212224ff" }} />);
    });
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
      {props.songs ? <List> {listItems()} </List> : <LinearProgress />}
    </Box>
  );
}

export default MusicList;
