import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";

const buttonStyle = {
  textTransform: "none",
  color: "#ffffff",
};

function AppHeader() {
  return (
    <AppBar position="fixed" sx={{ bgcolor: "#000000" }}>
      <Toolbar>
        <Typography variant="h6" component="span">
          jukebox.
        </Typography>
        <Button
          component={Link}
          to="/home/discover"
          sx={{ marginLeft: "2em", ...buttonStyle }}
        >
          <Typography variant="h6" component="span">
            discover
          </Typography>
        </Button>
        <Button component={Link} to="/home/listen" sx={buttonStyle}>
          <Typography variant="h6" component="span">
            listen
          </Typography>
        </Button>
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
