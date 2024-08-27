import { useCallback, useEffect, useState } from "react";
import styles from "./LoginPage.module.css";
import { Button, Link, Snackbar, TextField } from "@mui/material";
import Lottie from "lottie-react";
import animationData from "../../assets/animations/robot.json";
import GoogleIcon from "./components/GoogleIcon";
import { ANIMATION_CLICK_MAX_COUNT } from "./Constants";
import { useNavigate } from "react-router-dom";
import { PageNames } from "../../Navigation/PageNames";

const LoginPage = () => {
  const navigate = useNavigate();
  const [isError, setIsError] = useState(false);
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [animationClick, setAninationClick] = useState(0);

  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  const onSubmit = useCallback(() => {
    if (!password || !userName) {
      setSnackbarMessage("Kullanıcı adı ve şifre boş olamaz.");
      setSnackbarOpen(true);
      setIsError(true);
      return;
    }

    if (password.trim() !== "test" || userName.trim() !== "test") {
      setSnackbarMessage("Kullanıcı adı veya şifre yanlış.");
      setSnackbarOpen(true);
      setIsError(true);
      return;
    }

    navigate(PageNames.Home);
  }, [password, userName]);

  useEffect(() => {
    if (isError) {
      setIsError(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userName, password]);

  const onAnimationClicked = useCallback(() => {
    setAninationClick((prev) => prev + 1);
  }, [setAninationClick]);

  useEffect(() => {
    if (animationClick >= ANIMATION_CLICK_MAX_COUNT) {
      navigate(PageNames.Home);
    }
  }, [animationClick]);

  return (
    <div className={`${styles.container} ${styles.gradientBackground}`}>
      <div className={styles.loginContainer}>
        <div className={styles.animationContainer}>
          <Lottie
            onClick={onAnimationClicked}
            className={styles.animation}
            animationData={animationData}
            loop={true}
          />
        </div>
        <TextField
          className={styles.input}
          margin="normal"
          id="email"
          label="Kullanıcı Adı"
          name="username"
          autoComplete="username"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
          error={isError}
        />
        <TextField
          className={styles.input}
          margin="normal"
          id="password"
          type="password"
          label="Şifre"
          name="password"
          autoComplete="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={isError}
        />
        <Link
          sx={{ fontSize: "14px", fontFamily: "bold" }}
          className={styles.link}
        >
          Şifremi unuttum
        </Link>
        <Button
          onClick={onSubmit}
          className={styles.submitButton}
          type="submit"
          fullWidth
          sx={{ mt: 3, textTransform: "none" }}
          variant="contained"
        >
          Giriş Yap
        </Button>
        <Button
          variant="outlined"
          className={styles.submitButton}
          startIcon={<GoogleIcon />}
          fullWidth
          sx={{ mt: 2, textTransform: "none" }}
        >
          Google İle Gir
        </Button>
      </div>
      <Snackbar
        color="#ff0000"
        open={snackbarOpen}
        autoHideDuration={2000}
        onClose={handleSnackbarClose}
        message={snackbarMessage}
        sx={{
          "& .MuiSnackbarContent-root": {
            backgroundColor: "blue",
            color: "#FFFFFF",
          },
        }}
      />
    </div>
  );
};

export default LoginPage;
