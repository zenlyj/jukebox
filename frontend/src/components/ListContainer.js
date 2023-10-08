import Box from "@mui/material/Box";
import MusicList from "./MusicList";

function ListContainer(props) {
  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        bgcolor: "#141414ff",
        overflow: "auto",
        "&::-webkit-scrollbar": {
          backgroundColor: "#141414ff",
        },
        "&::-webkit-scrollbar-thumb": {
          backgroundColor: "#212224ff",
        },
      }}
    >
      <MusicList
        listHeader={props.listHeader}
        songs={props.songs}
        onClickHandler={props.onClickHandler}
      />
    </Box>
  );
}

export default ListContainer;
