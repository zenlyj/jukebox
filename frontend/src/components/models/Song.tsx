import { Genre } from "./Genre";

export interface Song {
  id: number;
  name: string;
  artistNames: string[];
  uri: string;
  albumCover: string;
  duration: number;
  genreName: Genre;
  timestamp: string;
}
