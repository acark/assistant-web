import { Routes, Route, Navigate } from "react-router-dom";
import { BrowserRouter as Router } from "react-router-dom";
import LoginPage from "../Pages/Login/LoginPage";
import HomePage from "../Pages/Home/HomePage";
import AboutPage from "../Pages/About/AboutPage";
import { PageNames } from "./PageNames";
import DrawerLayout from "./components/DrawerLayout";
import CompanyPage from "../Pages/Company/CompanyPage";
import CallPage from "../Pages/Call/CallPage";
import CalendarPage from "../Pages/Calendar/CalendarPage";

function AppRoutes() {
  return (
    <Routes>
      {/* Login Page Route */}
      <Route path={PageNames.Login} element={<LoginPage />} />

      <Route path="/" element={<DrawerLayout />}>
        <Route path={PageNames.Home} element={<HomePage />} />
        <Route path={PageNames.About} element={<AboutPage />} />
        <Route path={PageNames.Company} element={<CompanyPage />} />
        <Route path={PageNames.Call} element={<CallPage />} />
        <Route path={PageNames.Calendar} element={<CalendarPage />} />
      </Route>

      <Route path="*" element={<Navigate to={PageNames.Login} />} />
    </Routes>
  );
}

export default AppRoutes;
