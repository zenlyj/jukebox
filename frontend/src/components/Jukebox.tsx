import React, { useEffect, useReducer } from "react";
import MusicList from "./MusicList.tsx";
import { MusicListPagination } from "./MusicListPagination.tsx";
import { Song } from "./models/Song.tsx";
import {
  getSongsByDate,
  GetSongsByDateResponse,
} from "../api/GetSongsByDate.tsx";
import {
  addSongToPlaylist,
  AddSongToPlaylistResponse,
} from "../api/AddSongToPlaylist.tsx";
import { useOutletContext } from "react-router-dom";
import { HomeContext } from "./models/HomeContext.tsx";
import { Box } from "@mui/material";
import { ToggleButton } from "@mui/material";
import { ToggleButtonGroup } from "@mui/material";
import { getUserInfo } from "../utils/session.tsx";
import {
  GetRecommendedSongsResponse,
  getRecommendedSongs,
} from "../api/GetRecommendedSongs.tsx";
import { jbdarkgrey, jblightgrey, jbwhite } from "../utils/colors.tsx";
import RecommendIcon from "@mui/icons-material/Recommend";
import AccessTimeIcon from "@mui/icons-material/AccessTime";

enum OrderType {
  DATE = "DATE",
  RECOMMENDED = "RECOMMENDED",
}

interface State {
  songs: Song[];
  songCount: number;
  pageNum: number;
  order: OrderType;
}

enum ActionType {
  GET_SONGS,
  CHANGE_PAGE_NUMBER,
  CHANGE_ORDER,
}

interface GetRecommendedSongsAction {
  type: ActionType.GET_SONGS;
  songs: Song[];
  songCount: number;
}

interface ChangePageNumberAction {
  type: ActionType.CHANGE_PAGE_NUMBER;
  pageNum: number;
}

interface ChangeOrderAction {
  type: ActionType.CHANGE_ORDER;
  order: OrderType;
}

type Action =
  | GetRecommendedSongsAction
  | ChangePageNumberAction
  | ChangeOrderAction;

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case ActionType.GET_SONGS:
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
    case ActionType.CHANGE_ORDER:
      return {
        ...state,
        order: action.order,
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
    order: OrderType.RECOMMENDED,
  });

  const { playlistSize, setPlaylistSize, genre } =
    useOutletContext<HomeContext>();
  const pageSize = 10;

  useEffect(() => {
    let response: Promise<
      GetSongsByDateResponse | GetRecommendedSongsResponse
    > | null = null;
    if (state.order === OrderType.DATE) {
      response = getSongsByDate(genre, state.pageNum, pageSize);
    }
    if (state.order === OrderType.RECOMMENDED) {
      const userId = getUserInfo()?.userId;
      if (!userId) {
        return;
      }
      response = getRecommendedSongs(userId, genre, state.pageNum, pageSize);
    }
    if (!response) {
      return;
    }
    response.then(
      (response: GetSongsByDateResponse | GetRecommendedSongsResponse) => {
        dispatch({
          type: ActionType.GET_SONGS,
          songs: response.songs,
          songCount: response.songCount,
        });
      }
    );
  }, [state.pageNum, state.order]);

  const addToPlaylist = (songId: number): void => {
    const spotifyUserId = getUserInfo()?.userId;
    if (!spotifyUserId) {
      return;
    }
    addSongToPlaylist(spotifyUserId, songId).then(
      (response: AddSongToPlaylistResponse) => {
        if (response.isAdded) {
          console.log("Successfully added to playlist");
          setPlaylistSize(playlistSize + 1);
        } else {
          console.log("Failed to add to playlist");
        }
      }
    );
  };

  const handlePageChange = (event, pageNumber: number): void => {
    dispatch({ type: ActionType.CHANGE_PAGE_NUMBER, pageNum: pageNumber });
  };

  const getPageCount = (): number => {
    return Math.ceil(state.songCount / pageSize);
  };

  const handleOrderChange = (event, newOrder: OrderType | null) => {
    dispatch({
      type: ActionType.CHANGE_ORDER,
      order: newOrder ?? OrderType.RECOMMENDED,
    });
  };

  const toggleButtonStyle = (order: OrderType): Object => ({
    "&.MuiToggleButton-root, &.Mui-selected, &.Mui-selected:hover": {
      color: state.order === order ? jbwhite : jblightgrey,
      backgroundColor: jbdarkgrey,
    },
  });

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
      <ToggleButtonGroup
        value={state.order}
        exclusive
        onChange={handleOrderChange}
      >
        <ToggleButton
          value={OrderType.RECOMMENDED}
          sx={toggleButtonStyle(OrderType.RECOMMENDED)}
        >
          <RecommendIcon />
        </ToggleButton>
        <ToggleButton
          value={OrderType.DATE}
          sx={toggleButtonStyle(OrderType.DATE)}
        >
          <AccessTimeIcon />
        </ToggleButton>
      </ToggleButtonGroup>
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
