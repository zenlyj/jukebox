import { Genre } from "./Genre";

export interface HomeContext {
  playlistSize: number;
  setPlaylistSize: React.Dispatch<React.SetStateAction<number>>;
  genre: Genre;
}
