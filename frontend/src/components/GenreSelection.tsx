import React from "react";
import { Box } from "@mui/material";
import { Card } from "@mui/material";
import { CardContent } from "@mui/material";
import { CardMedia } from "@mui/material";
import { Typography } from "@mui/material";
import { CardActionArea } from "@mui/material";
import {
  electronicGenreImage,
  generalGenreImage,
  hiphopGenreImage,
} from "../utils/images.tsx";
import { _ } from "../utils/libs.tsx";
import { Genre } from "./models/Genre.tsx";

interface Props {
  setGenre: (genre: Genre) => void;
}

export function GenreSelection(props: Props) {
  const images = [hiphopGenreImage, electronicGenreImage, generalGenreImage];
  const headers = ["hiphop.", "electronic.", "general."];
  const bodies = [
    "Browse tracks from r/hiphopheads",
    "Browse tracks from r/electronicmusic",
    "Browse tracks of any genre",
  ];
  const genres = [Genre.HIPHOP, Genre.ELECTRONIC, Genre.GENERAL];

  const card = (image, header: string, body: string, genre: Genre) => {
    return (
      <Card sx={{ maxWidth: 300 }}>
        <CardActionArea onClick={() => props.setGenre(genre)}>
          <CardMedia
            component="img"
            height="250"
            width="250"
            image={image}
            alt="Image not loaded"
          />
          <CardContent sx={{ bgcolor: "#141414ff", opacity: "90%" }}>
            <Typography
              sx={{ color: "#ffffff" }}
              gutterBottom
              variant="h5"
              component="div"
            >
              {header}
            </Typography>
            <Typography variant="body2" color="#a1a1a1ff">
              {body}
            </Typography>
          </CardContent>
        </CardActionArea>
      </Card>
    );
  };

  return (
    <Box sx={{ display: "flex", columnGap: "10rem", justifyContent: "center" }}>
      {_.zip(images, headers, bodies, genres).map((cardInfo) =>
        card(cardInfo[0], cardInfo[1], cardInfo[2], cardInfo[3])
      )}
    </Box>
  );
}
