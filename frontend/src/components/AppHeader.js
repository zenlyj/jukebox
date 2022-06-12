import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import HeadphonesIcon from "@mui/icons-material/Headphones";

function AppHeader() {
  return (
    <AppBar position="fixed" sx={{ bgcolor: "#000000" }}>
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <HeadphonesIcon />
        </IconButton>
        <Typography variant="h6" component="span" sx={{ flexGrow: 1 }}>
          jukebox.
        </Typography>
        <Typography
          variant="h6"
          component="span"
          sx={{ flexGrow: 1 }}
          align="right"
        >
          v0.1.0
        </Typography>
      </Toolbar>
    </AppBar>
  );
}

export default AppHeader;
