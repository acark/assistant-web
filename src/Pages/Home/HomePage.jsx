import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Button,
  Modal,
} from "@mui/material";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import AddIcon from "@mui/icons-material/Add";

const dummyReservations = [
  {
    id: 1,
    name: "John Doe",
    phone: "+123456789",
    date: "2024-08-25",
  },
  {
    id: 2,
    name: "Jane Smith",
    phone: "+987654321",
    date: "2024-08-26",
  },
  {
    id: 3,
    name: "Alice Johnson",
    phone: "+192837465",
    date: "2024-08-27",
  },
  // Add more dummy data as needed
];

const chartData = {
  labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  datasets: [
    {
      label: "Calls Per Day",
      data: [12, 19, 3, 5, 2, 3, 7],
      backgroundColor: "#0357D1",
    },
  ],
};

const HomePage = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [reservations, setReservations] = useState(dummyReservations);

  const handleAccept = (id) => {
    console.log(`Accepted reservation with id ${id}`);
    // Implement the logic to accept the reservation
  };

  const handleRefuse = (id) => {
    console.log(`Refused reservation with id ${id}`);
    // Implement the logic to refuse the reservation
  };

  const filteredReservations = reservations.filter((reservation) =>
    reservation.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const paperStyle = {
    p: 2,
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    height: "150px", // Fixed height
    boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)", // Slight shadow
    opacity: 0.9, // Slight opacity
  };

  return (
    <Box sx={{ p: 2 }}>
      {/* Top Information Section */}
      <Grid container spacing={2} mb={4}>
        <Grid item xs={12} sm={3}>
          <Paper sx={{ ...paperStyle, bgcolor: "#0357D1", color: "#fff" }}>
            <Typography variant="h6">Toplam Arama</Typography>
            <Typography variant="h4">150</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Paper sx={{ ...paperStyle, bgcolor: "#D14124", color: "#fff" }}>
            <Typography variant="h6">Masraf</Typography>
            <Typography variant="h4">₺1240</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Paper sx={{ ...paperStyle, bgcolor: "#28a745", color: "#fff" }}>
            <Typography variant="h6">Toplama Arama Süresi</Typography>
            <Typography variant="h4">143 Dakika</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Paper sx={{ ...paperStyle, bgcolor: "#2196F3", color: "#fff" }}>
            <Typography variant="h6">Rezervayon Sayısı</Typography>
            <Typography variant="h4">102</Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Search Bar and Add Reservation Button */}
      <Box sx={{ display: "flex", flex: 1, alignItems: "center", mb: 4 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Rezervasyonlarda Ara..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ mr: 2, display: "flex", flex: 5 }}
        />
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          sx={{ height: "56px", display: "flex", flex: 1 }}
        >
          Rezervasyon Ekle
        </Button>
      </Box>

      {/* Reservation List Section */}
      <List>
        {filteredReservations.map((reservation) => (
          <ListItem key={reservation.id} sx={{ mb: 2, bgcolor: "#f0f0f0" }}>
            <ListItemText
              primary={reservation.name}
              secondary={`Telefon: ${reservation.phone} - Tarih: ${reservation.date}`}
            />
            <ListItemSecondaryAction>
              <IconButton
                edge="end"
                aria-label="accept"
                color="primary"
                sx={{ mr: 5 }}
                onClick={() => handleAccept(reservation.id)}
              >
                <CheckIcon />
              </IconButton>
              <IconButton
                edge="end"
                aria-label="refuse"
                color="secondary"
                sx={{ mr: 5 }}
                onClick={() => handleRefuse(reservation.id)}
              >
                <CloseIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default HomePage;
