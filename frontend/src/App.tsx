import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./Home.tsx";
import SpotifyAuth from "./SpotifyAuth.tsx";
import Jukebox from "./components/Jukebox.tsx";
import Playlist from "./components/Playlist.tsx";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<SpotifyAuth />} />
        <Route path="/home" element={<Home />}>
          <Route path="discover" element={<Jukebox />} />
          <Route path="listen" element={<Playlist />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
