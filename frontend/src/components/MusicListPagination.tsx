import React from "react";
import { Container, Pagination } from "@mui/material";
import { jbwhite } from "../utils/colors.tsx";

interface Props {
  pageCount: number;
  pageNum: number;
  handlePageChange: (event, page: number) => void;
}

export function MusicListPagination(props: Props) {
  return (
    <Container sx={{ display: "flex", justifyContent: "center" }}>
      <Pagination
        color="primary"
        sx={{
          button: { color: jbwhite },
          div: { color: jbwhite, opacity: 0.38 },
        }}
        count={props.pageCount}
        page={props.pageNum}
        onChange={props.handlePageChange}
      />
    </Container>
  );
}
