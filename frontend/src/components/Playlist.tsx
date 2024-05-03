import React, { useEffect, useReducer } from "react";
import { Box } from "@mui/material";
import MusicList from "./MusicList.tsx";
import { Song } from "./models/Song.tsx";
import {
  deletePlaylistSong,
  DeletePlaylistSongResponse,
} from "../api/DeletePlaylistSong.tsx";
import { getPlaylist, GetPlaylistResponse } from "../api/GetPlaylist.tsx";
import SpotifyPlayer, { Props } from "react-spotify-web-playback";
import { useOutletContext } from "react-router-dom";
import { HomeContext } from "./models/HomeContext.tsx";
import { MusicListPagination } from "./MusicListPagination.tsx";
import {
  refreshAccessToken,
  RefreshAccessTokenResponse,
} from "../api/RefreshAccessToken.tsx";
import {
  getAccessToken,
  getTokenExpireTime,
  getTokenExpiresIn,
  setAccessToken,
  setTokenExpireTime,
  setTokenExpiresIn,
} from "../utils/session.tsx";

interface State {
  songs: Song[];
  uris: string[];
  songCount: number;
  pageNum: number;
}

enum ActionType {
  GET_PLAYLIST_SONGS,
  CHANGE_PAGE_NUMBER,
}

interface GetPlaylistSongsAction {
  type: ActionType.GET_PLAYLIST_SONGS;
  songs: Song[];
  uris: string[];
  songCount: number;
  pageNum: number;
}

interface ChangePageNumberAction {
  type: ActionType.CHANGE_PAGE_NUMBER;
  pageNum: number;
}

type Action = GetPlaylistSongsAction | ChangePageNumberAction;

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case ActionType.GET_PLAYLIST_SONGS:
      return {
        ...state,
        songs: action.songs,
        uris: action.uris,
        songCount: action.songCount,
        pageNum: action.pageNum,
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

function Playlist() {
  const [state, dispatch] = useReducer(reducer, {
    songs: [],
    uris: [],
    songCount: 0,
    pageNum: 1,
  });
  const { setPlaylistSize } = useOutletContext<HomeContext>();
  const pageSize = 10;

  useEffect(() => {
    getPlaylistSongs(state.pageNum);
  }, [state.pageNum]);

  const getPlaylistSongs = (pageNum: number): void => {
    getPlaylist(pageNum, pageSize).then((response: GetPlaylistResponse) => {
      dispatch({
        type: ActionType.GET_PLAYLIST_SONGS,
        songs: response.songs,
        uris: response.songs.map((song) => song.uri),
        songCount: response.playlistSize,
        pageNum: pageNum,
      });
      setPlaylistSize(response.playlistSize);
    });
  };

  const removePlaylistSong = (songId: number): void => {
    deletePlaylistSong(songId).then((response: DeletePlaylistSongResponse) => {
      if (response.isDeleted) {
        console.log("Successfully removed song from playlist");
        const updatedPageNum =
          state.songs.length === 1 && state.pageNum > 1
            ? state.pageNum - 1
            : state.pageNum;
        getPlaylistSongs(updatedPageNum);
      } else {
        console.log("Failed to delete");
      }
    });
  };

  const handlePageChange = (event, pageNumber: number): void => {
    dispatch({ type: ActionType.CHANGE_PAGE_NUMBER, pageNum: pageNumber });
  };

  const getPageCount = (): number => {
    return Math.ceil(state.songCount / pageSize);
  };

  const getOAuthToken: Props["getOAuthToken"] = async (callback) => {
    const accessToken = getAccessToken();
    if (!accessToken) {
      return;
    }
    if (getTokenExpireTime() > Date.now()) {
      callback(accessToken);
      return;
    }
    refreshAccessToken(accessToken).then(
      (response: RefreshAccessTokenResponse) => {
        if (!response.accessToken) {
          return;
        }
        setAccessToken(response.accessToken);
        setTokenExpiresIn(response.expiresIn);
        setTokenExpireTime(Date.now() + getTokenExpiresIn() * 1000);
        callback(response.accessToken);
      }
    );
  };

  return (
    <Box sx={{ height: "100%" }}>
      <Box sx={{ height: "90%", overflow: "auto" }}>
        <Box
          sx={{
            padding: "1rem",
            display: "flex",
            flexDirection: "column",
            height: "100%",
            justifyContent: "space-between",
          }}
        >
          <MusicList songs={state.songs} onClickHandler={removePlaylistSong} />
          <MusicListPagination
            pageCount={getPageCount()}
            pageNum={state.pageNum}
            handlePageChange={handlePageChange}
          />
        </Box>
      </Box>
      <Box
        sx={{
          height: "10%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-end",
        }}
      >
        <SpotifyPlayer
          getOAuthToken={getOAuthToken}
          token={getAccessToken() ?? ""}
          uris={state.uris}
        />
      </Box>
    </Box>
  );
}

export default Playlist;
