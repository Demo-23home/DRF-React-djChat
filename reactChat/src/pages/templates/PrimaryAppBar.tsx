import { AppBar, Toolbar } from "@mui/material";
import { useTheme } from "@mui/material/styles";

const PrimaryAppBar = () => {
  const theme = useTheme();
  const appBarHeight = theme.primaryAppBar.height || 0

  return (
    <>
      <AppBar>
        <Toolbar variant="dense" sx={{ height: appBarHeight }}>
          a
        </Toolbar>
      </AppBar>
    </>
  );
};

export default PrimaryAppBar;
