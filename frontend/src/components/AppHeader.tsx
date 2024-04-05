import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Badge, Button } from "@mui/material";
import { Link } from "react-router-dom";

const buttonStyle = {
  textTransform: "none",
  color: "#ffffff",
};

interface Props {
  playlistSize: number;
}

function AppHeader(props: Props) {
  return (
    <AppBar position="fixed" sx={{ bgcolor: "#010409" }}>
      <Toolbar>
        <Typography variant="h6" component="span">
          jukebox.
        </Typography>
        <Button
          size="small"
          component={Link}
          to="/home/discover"
          sx={{ marginLeft: "2em", ...buttonStyle }}
        >
          <Typography variant="h6" component="span">
            discover
          </Typography>
        </Button>
        <Badge badgeContent={props.playlistSize} color="primary">
          <Button
            size="small"
            component={Link}
            to="/home/listen"
            sx={buttonStyle}
          >
            <Typography variant="h6" component="span">
              listen
            </Typography>
          </Button>
        </Badge>
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
