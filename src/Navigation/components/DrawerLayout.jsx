import React from "react";
import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import HomeIcon from "@mui/icons-material/Home";
import Calendar from "@mui/icons-material/CalendarMonth";
import Phone from "@mui/icons-material/Phone";
import { Outlet, Link, useLocation } from "react-router-dom";
import Typography from "@mui/material/Typography";
import Avatar from "@mui/material/Avatar";
import Lottie from "lottie-react";
import animationData from "../../assets/animations/robot.json";
import Company from "@mui/icons-material/Work";
import About from "@mui/icons-material/QuestionMark";
import { PageNames } from "../PageNames";

const drawerWidth = 240;

const drawerItems = [
  { text: "Anasayfa", icon: <HomeIcon />, path: PageNames.Home },
  { text: "İşletme", icon: <Company />, path: PageNames.Company },
  { text: "Takvim", icon: <Calendar />, path: PageNames.Calendar },
  { text: "Arama", icon: <Phone />, path: PageNames.Call },
  { text: "Hakkımızda", icon: <About />, path: PageNames.About },
];

function DrawerLayout(props) {
  const { window } = props;
  const location = useLocation(); // Get current route

  const drawer = (
    <Box
      sx={{
        textAlign: "center",
        bgcolor: "#3F51B5", // Updated drawer background color
        height: "100vh",
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          my: 2,
          gap: 2,
        }}
      >
        <Lottie
          animationData={animationData}
          loop
          style={{ width: 40, height: 40 }}
        />
        <Typography variant="h5" sx={{ color: "#fff", marginLeft: -1 }}>
          Asistan
        </Typography>
      </Box>
      <Box sx={{ my: 6 }}>
        <Avatar
          sx={{
            bgcolor: "#ffffff33",
            width: 64,
            height: 64,
            mx: "auto",
            my: 1,
          }}
        >
          T
        </Avatar>
        <Typography variant="body1" sx={{ color: "#fff", my: 1 }}>
          test
        </Typography>
      </Box>
      <List>
        {drawerItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <ListItem key={item.text}>
              <ListItemButton
                component={Link}
                to={item.path}
                sx={{
                  color: "#fff",
                  justifyContent: "center",
                  //textAlign: "center",
                  bgcolor: isActive ? "#9FA8DA" : "transparent",
                  "&:hover": {
                    bgcolor: "#9FA8DA",
                  },
                  borderRadius: 5,
                }}
              >
                <ListItemIcon sx={{ color: "#fff", justifyContent: "center" }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item?.text} />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </Box>
  );

  const container =
    window !== undefined ? () => window().document.body : undefined;

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <Box
        component="nav"
        sx={{
          width: { sm: drawerWidth },
          flexShrink: { sm: 0 },
        }}
        aria-label="mailbox folders"
      >
        <Drawer
          container={container}
          variant="persistent"
          open={true}
          sx={{
            display: { xs: "block", sm: "block" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth,
              transition: "width 0.3s",
              backgroundColor: "#0D47A1",
            },
          }}
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          transition: "width 0.3s",
          bgcolor: "#ffffff", // Background color for content area
          minHeight: "100vh",
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
}

DrawerLayout.propTypes = {
  window: PropTypes.func,
};

export default DrawerLayout;
