import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./Home.tsx";
import SpotifyAuth from "./SpotifyAuth.tsx";

function App() {
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
