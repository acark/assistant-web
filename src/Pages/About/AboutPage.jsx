import React from "react";
import {
  Box,
  Typography,
  Avatar,
  Grid,
  IconButton,
  Paper,
} from "@mui/material";
import FacebookIcon from "@mui/icons-material/Facebook";
import TwitterIcon from "@mui/icons-material/Twitter";
import InstagramIcon from "@mui/icons-material/Instagram";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import InfoIcon from "@mui/icons-material/Info";

const AboutPage = () => {
  return (
    <Box
      sx={{
        p: 4,
        background: "linear-gradient(to right, #FFFFFF, #FFFFFF)",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: 4,
          bgcolor: "#f5f5f5",
          borderRadius: 2,
          maxWidth: 800,
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            mb: 4,
            justifyContent: "center",
          }}
        >
          <Avatar
            sx={{
              bgcolor: "#1976d2",
              width: 64,
              height: 64,
              mr: 2,
            }}
          >
            <InfoIcon fontSize="large" />
          </Avatar>
          <Typography variant="h4" sx={{ color: "#333", textAlign: "center" }}>
            Hakkımızda
          </Typography>
        </Box>

        <Typography
          variant="body1"
          sx={{ color: "#555", mb: 4, mr: 10, ml: 10, textAlign: "center" }}
        >
          Şirketimiz, müşterilerimize en iyi hizmeti sunmayı amaçlayan bir
          teknoloji şirketidir. Misyonumuz, kullanıcılarımızın günlük
          ihtiyaçlarına en iyi çözümleri sunarak hayatlarını kolaylaştırmaktır.
          Yenilikçi ve kullanıcı odaklı yaklaşımımızla, her zaman en kaliteli
          hizmeti sunmayı hedefliyoruz.
        </Typography>

        <Grid container spacing={2} justifyContent="center" sx={{ mb: 4 }}>
          <Grid item>
            <IconButton
              href="https://facebook.com"
              target="_blank"
              sx={{ color: "#3b5998" }}
            >
              <FacebookIcon fontSize="large" />
            </IconButton>
          </Grid>
          <Grid item>
            <IconButton
              href="https://twitter.com"
              target="_blank"
              sx={{ color: "#00acee" }}
            >
              <TwitterIcon fontSize="large" />
            </IconButton>
          </Grid>
          <Grid item>
            <IconButton
              href="https://instagram.com"
              target="_blank"
              sx={{ color: "#c13584" }}
            >
              <InstagramIcon fontSize="large" />
            </IconButton>
          </Grid>
          <Grid item>
            <IconButton
              href="https://linkedin.com"
              target="_blank"
              sx={{ color: "#0e76a8" }}
            >
              <LinkedInIcon fontSize="large" />
            </IconButton>
          </Grid>
        </Grid>

        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            flexDirection: "column",
          }}
        >
          <Typography variant="h6" sx={{ color: "#333", mb: 2 }}>
            İletişim
          </Typography>
          <Typography variant="body1" sx={{ color: "#555" }}>
            Email: acar15k@gmail.com
          </Typography>
          <Typography variant="body1" sx={{ color: "#555" }}>
            Telefon: +90 530 775 49 60
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
};

export default AboutPage;
