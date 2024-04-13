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
import { getMonthName, padNum } from "../utils/datetime.tsx";

interface Props {
  songs: Song[];
  displayDate?: boolean;
  onClickHandler: (songId: number, songUri: string) => void;
}

function MusicList(props: Props) {
  const formatArtistNames = (artistNames: string[]): string => {
    return artistNames.join(", ");
  };

  const formatDuration = (duration: number): string => {
    const totalSeconds = duration / 1000;
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = Math.floor(totalSeconds - minutes * 60);
    return `${minutes}:${padNum(seconds)}`;
  };

  const formatTimestamp = (timestamp: string): string => {
    const date = new Date(parseInt(timestamp) * 1000);
    const year = date.getFullYear();
    const month = date.getMonth();
    const day = date.getDate();
    const hour = date.getHours();
    const min = date.getMinutes();
    return `${padNum(day)}-${getMonthName(month)}-${year} - ${padNum(
      hour
    )}:${padNum(min)}`;
  };

  const listItem = (song: Song): React.JSX.Element => (
    <ListItem disablePadding key={song.id}>
      <ListItemButton
        onClick={() => props.onClickHandler(song.id, song.uri)}
        sx={{
          "&:hover": {
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
        <Box sx={{ display: "flex", columnGap: "2rem" }}>
          {props.displayDate ? (
            <ListItemText
              secondary={formatTimestamp(song.timestamp)}
              secondaryTypographyProps={{
                color: "#a1a1a1ff",
              }}
            />
          ) : null}
          <ListItemText
            secondary={formatDuration(song.duration)}
            secondaryTypographyProps={{
              color: "#a1a1a1ff",
            }}
          />
        </Box>
      </ListItemButton>
    </ListItem>
  );

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
      {!props.songs ? (
        <LinearProgress />
      ) : (
        <List>
          {props.songs.map((song) => (
            <React.Fragment>
              {listItem(song)}
              <Divider sx={{ bgcolor: "#212224ff" }} />
            </React.Fragment>
          ))}
        </List>
      )}
    </Box>
  );
}

export default MusicList;
