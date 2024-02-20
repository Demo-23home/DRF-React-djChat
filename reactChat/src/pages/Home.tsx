import { Box, CssBaseline } from "@mui/material";
import PrimaryAppBar from "./templates/PrimaryAppBar";
import { useTheme } from "@mui/material/styles";

const Home = () => {
  const theme = useTheme(); 
  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <PrimaryAppBar />
    </Box>
  );
};

export default Home;
