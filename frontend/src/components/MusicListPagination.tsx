import React from "react";
import { Container, Pagination } from "@mui/material";

interface Props {
  pageCount: number;
  handlePageChange: (event, page: number) => void;
}

export function MusicListPagination(props: Props) {
  return (
    <Container sx={{ display: "flex", justifyContent: "center" }}>
      <Pagination
        color="primary"
        sx={{
          button: { color: "#ffffff" },
          div: { color: "#ffffff", opacity: 0.38 },
        }}
        count={props.pageCount}
        onChange={props.handlePageChange}
      />
    </Container>
  );
}
