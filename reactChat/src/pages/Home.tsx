import { Box, CssBaseline } from "@mui/material";
import PrimaryAppBar from "./templates/PrimaryAppBar";
import { useTheme } from "@mui/material/styles";
import PrimaryDrawer from "./templates/PrimaryDraw";

const Home = () => {
  const theme = useTheme(); 
  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <PrimaryAppBar />
      <PrimaryDrawer>
        
      </PrimaryDrawer>
    </Box>
  );
};

export default Home;
