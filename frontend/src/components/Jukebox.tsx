import React, { useEffect, useReducer } from "react";
import MusicList from "./MusicList.tsx";
import { MusicListPagination } from "./MusicListPagination.tsx";
import { Song } from "./models/Song.tsx";
import { getSongs, GetSongsResponse } from "../api/GetSongs.tsx";
import {
  addSongToPlaylist,
  AddSongToPlaylistResponse,
} from "../api/AddSongToPlaylist.tsx";
import { useOutletContext } from "react-router-dom";
import { HomeContext } from "./models/HomeContext.tsx";
import { Box } from "@mui/material";

interface State {
  songs: Song[];
  songCount: number;
  pageNum: number;
}

enum ActionType {
  GET_RECOMMENDED_SONGS,
  CHANGE_PAGE_NUMBER,
}

interface GetRecommendedSongsAction {
  type: ActionType.GET_RECOMMENDED_SONGS;
  songs: Song[];
  songCount: number;
}

interface ChangePageNumberAction {
  type: ActionType.CHANGE_PAGE_NUMBER;
  pageNum: number;
}

type Action = GetRecommendedSongsAction | ChangePageNumberAction;

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case ActionType.GET_RECOMMENDED_SONGS:
      return {
        ...state,
        songs: action.songs,
        songCount: action.songCount,
      };
    case ActionType.CHANGE_PAGE_NUMBER:
      return {
        ...state,
        pageNum: action.pageNum,
      };
    default:
      return state;
  }
}

function Jukebox() {
  const [state, dispatch] = useReducer(reducer, {
    songs: [],
    songCount: 0,
    pageNum: 1,
  });

  const { playlistSize, setPlaylistSize, genre } =
    useOutletContext<HomeContext>();
  const pageSize = 10;

  useEffect(() => {
    getRecommendedSongs(state.pageNum);
  }, [state.pageNum]);

  const getRecommendedSongs = (pageNum: number) => {
    getSongs(genre, pageNum, pageSize).then((response: GetSongsResponse) => {
      dispatch({
        type: ActionType.GET_RECOMMENDED_SONGS,
        songs: response.songs,
        songCount: response.songCount,
      });
    });
  };

  const addToPlaylist = (songId: number): void => {
    addSongToPlaylist(songId).then((response: AddSongToPlaylistResponse) => {
      if (response.isAdded) {
        console.log("Successfully added to playlist");
        setPlaylistSize(playlistSize + 1);
      } else {
        console.log("Failed to add to playlist");
      }
    });
  };

  const handlePageChange = (event, pageNumber: number): void => {
    dispatch({ type: ActionType.CHANGE_PAGE_NUMBER, pageNum: pageNumber });
  };

  const getPageCount = (): number => {
    return Math.ceil(state.songCount / pageSize);
  };

  return (
    <Box
      sx={{
        padding: "1rem",
        display: "flex",
        flexDirection: "column",
        height: "100%",
        justifyContent: "space-between",
      }}
    >
      <MusicList
        songs={state.songs}
        displayDate={true}
        onClickHandler={addToPlaylist}
      />
      <MusicListPagination
        pageCount={getPageCount()}
        pageNum={state.pageNum}
        handlePageChange={handlePageChange}
      />
    </Box>
  );
}

export default Jukebox;
