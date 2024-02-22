import { AppBar, Link, Toolbar, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";

const PrimaryAppBar = () => {
  const theme = useTheme();
  const appBarHeight = theme.primaryAppBar.height || 0;

  return (
    <>
      <AppBar
        sx={{
          backgroundColor: theme.palette.background.default,
          borderBottom: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Toolbar
          variant="dense"
          sx={{ height: appBarHeight, minHeight: appBarHeight }}
        >
          <Link href="/" underline="none" color="inherit">
            <Typography
              variant="h6"
              noWrap
              component="div"
              sx={{ display: { fontWeigt: 700, letterSpacing: "-0.5px" } }}
            >
              DJCHAT
            </Typography>
          </Link>
        </Toolbar>
      </AppBar>
    </>
  );
};

export default PrimaryAppBar;
