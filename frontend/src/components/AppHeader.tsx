import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Badge, Button } from "@mui/material";
import { Link } from "react-router-dom";
import { Genre } from "./models/Genre.tsx";
import { Mode } from "./models/Mode.tsx";
import { jbblack, jblightgrey, jbwhite } from "../utils/colors.tsx";

interface Props {
  playlistSize: number;
  currMode: Mode;
  setGenre: (genre: Genre | null) => void;
  setMode: (mode: Mode) => void;
}

function AppHeader(props: Props) {
  const buttonStyle = {
    textTransform: "none",
    color: jbwhite,
  };

  const getModeTextColor = (mode: Mode): string =>
    props.currMode === mode ? jbwhite : jblightgrey;

  return (
    <AppBar position="fixed" sx={{ backgroundColor: jbblack }}>
      <Toolbar>
        <Typography variant="h6" component="span">
          jukebox.
        </Typography>
        <Button
          size="small"
          component={Link}
          to="/home/discover"
          onClick={() => {
            props.setGenre(null);
            props.setMode(Mode.DISCOVER);
          }}
          sx={{ marginLeft: "2em", ...buttonStyle }}
        >
          <Typography
            variant="h6"
            component="span"
            sx={{ color: getModeTextColor(Mode.DISCOVER) }}
          >
            discover
          </Typography>
        </Button>
        <Badge badgeContent={props.playlistSize} color="primary">
          <Button
            size="small"
            component={Link}
            to="/home/listen"
            onClick={() => {
              props.setGenre(null);
              props.setMode(Mode.LISTEN);
            }}
            sx={buttonStyle}
          >
            <Typography
              variant="h6"
              component="span"
              sx={{
                color: getModeTextColor(Mode.LISTEN),
              }}
            >
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
          v0.2.0
        </Typography>
      </Toolbar>
    </AppBar>
  );
}

export default AppHeader;
