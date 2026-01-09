// src/hooks/useAuth.js

import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { logout as reduxLogout } from "../redux/authSlice";

export default function useAuth() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  // Redux state
  const auth = useSelector((state) => state.auth);

  // ===== Fallback-safe values (important on refresh) =====
  const token =
    auth.accessToken || localStorage.getItem("access_token");

  const role =
    auth.role || localStorage.getItem("role");

  const isAuthenticated = !!token;

  // ===== Logout handler =====
  const logout = () => {
    dispatch(reduxLogout()); // clears redux + localStorage
    navigate("/login");
  };

  return {
    isAuthenticated,
    role,
    token,
    logout,
  };
}
