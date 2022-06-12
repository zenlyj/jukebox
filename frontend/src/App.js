import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Home from "./Home";
import SpotifyAuth from "./SpotifyAuth";

function App(props) {
  return (
    <div>
      <Routes>
        <Route path="/" element={<SpotifyAuth />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </div>
  );
}

export default App;
