import { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Grid,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  TextField,
  Button,
  IconButton,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DeleteIcon from "@mui/icons-material/Delete";

const CompanyPage = () => {
  const [businessStatus, setBusinessStatus] = useState("açık");
  const [workingHours, setWorkingHours] = useState({
    monday: { start: "00:00", end: "00:00" },
    tuesday: { start: "00:00", end: "00:00" },
    wednesday: { start: "00:00", end: "00:00" },
    thursday: { start: "00:00", end: "00:00" },
    friday: { start: "00:00", end: "00:00" },
    saturday: { start: "00:00", end: "00:00" },
    sunday: { start: "00:00", end: "00:00" },
  });
  const [uploadedFile, setUploadedFile] = useState(null);

  const handleBusinessStatusSave = () => {
    console.log("Business Status Saved:", businessStatus);
  };

  const handleWorkingHoursChange = (day, field, value) => {
    setWorkingHours({
      ...workingHours,
      [day]: { ...workingHours[day], [field]: value },
    });
  };

  const handleWorkingHoursSave = () => {
    console.log("Working Hours Saved:", workingHours);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setUploadedFile(file);
  };

  const handleFileRemove = () => {
    setUploadedFile(null);
  };

  const handleFileSave = () => {
    if (uploadedFile) {
      // Save file logic
      console.log("File Saved:", uploadedFile);
    } else {
      console.log("No file to save.");
    }
  };

  return (
    <Box sx={{ p: 4, mt: 4 }}>
      {/* Section 1: İşletme Durumu */}
      <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
        <Box>
          <Typography variant="h5" sx={{ mb: 3 }}>
            İşletme Durumu
          </Typography>
          <FormControl component="fieldset">
            <FormLabel component="legend">Durum</FormLabel>
            <RadioGroup
              row
              value={businessStatus}
              onChange={(e) => setBusinessStatus(e.target.value)}
            >
              <FormControlLabel value="açık" control={<Radio />} label="Açık" />
              <FormControlLabel
                value="kapalı"
                control={<Radio />}
                label="Kapalı"
              />
            </RadioGroup>
          </FormControl>
        </Box>
        <Button
          variant="contained"
          color="primary"
          onClick={handleBusinessStatusSave}
          sx={{ mt: 3 }}
        >
          Kaydet
        </Button>
      </Paper>

      {/* Section 2: Çalışma Saatleri */}
      <Paper elevation={3} sx={{ p: 4, mb: 4, position: "relative" }}>
        <Typography variant="h5" sx={{ mb: 3 }}>
          Çalışma Saatleri
        </Typography>
        <Grid container spacing={2}>
          {Object.entries(workingHours).map(([day, times]) => (
            <Grid item xs={12} sm={6} md={4} key={day}>
              <Typography
                variant="subtitle1"
                sx={{ mb: 1, textTransform: "capitalize" }}
              >
                {day}
              </Typography>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <TextField
                    label="Başlangıç"
                    type="time"
                    value={times.start}
                    onChange={(e) =>
                      handleWorkingHoursChange(day, "start", e.target.value)
                    }
                    InputLabelProps={{ shrink: true }}
                    inputProps={{ step: 300 }} // 5 min
                    fullWidth
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    label="Bitiş"
                    type="time"
                    value={times.end}
                    onChange={(e) =>
                      handleWorkingHoursChange(day, "end", e.target.value)
                    }
                    InputLabelProps={{ shrink: true }}
                    inputProps={{ step: 300 }}
                    fullWidth
                  />
                </Grid>
              </Grid>
            </Grid>
          ))}
        </Grid>
        <Button
          variant="contained"
          color="primary"
          onClick={handleWorkingHoursSave}
          sx={{ mt: 4 }}
        >
          Kaydet
        </Button>
      </Paper>

      {/* Section 3: İşletme Bilgileri Yükle */}
      <Paper elevation={3} sx={{ p: 4, position: "relative" }}>
        <Typography variant="h5" sx={{ mb: 3 }}>
          İşletme Bilgileri Yükle
        </Typography>
        <Box
          sx={{
            border: "2px dashed #aaa",
            borderRadius: 2,
            p: 4,
            textAlign: "center",
            backgroundColor: "#f9f9f9",
          }}
        >
          {!uploadedFile ? (
            <>
              <CloudUploadIcon sx={{ fontSize: 50, color: "#aaa", mb: 2 }} />
              <Typography variant="body1" sx={{ mb: 2 }}>
                İşletme hakkında bilgi içeren bir dosya yükleyin.
              </Typography>
              <Button variant="contained" component="label">
                Dosya Seçin
                <input type="file" hidden onChange={handleFileUpload} />
              </Button>
            </>
          ) : (
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Typography variant="body1" sx={{ mr: 2 }}>
                {uploadedFile.name}
              </Typography>
              <IconButton color="error" onClick={handleFileRemove}>
                <DeleteIcon />
              </IconButton>
            </Box>
          )}
        </Box>
        <Button
          variant="contained"
          color="primary"
          onClick={handleFileSave}
          sx={{ mt: 3 }}
          disabled={!uploadedFile}
        >
          Kaydet
        </Button>
      </Paper>
    </Box>
  );
};

export default CompanyPage;
