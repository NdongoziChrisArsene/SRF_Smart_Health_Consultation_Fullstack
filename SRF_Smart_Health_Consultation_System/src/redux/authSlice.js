import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  token: localStorage.getItem("access_token") || null,
  refreshToken: localStorage.getItem("refresh_token") || null,
  role: localStorage.getItem("role") || null,
  isAuthenticated: !!localStorage.getItem("access_token"),
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCredentials: (state, action) => {
      const { access, refresh, role } = action.payload;
      state.token = access;
      state.refreshToken = refresh;
      state.role = role;
      state.isAuthenticated = true;

      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      localStorage.setItem("role", role);
    },
    logout: (state) => {
      state.token = null;
      state.refreshToken = null;
      state.role = null;
      state.isAuthenticated = false;

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("role");
    },
  },
});

export const { setCredentials, logout } = authSlice.actions;
export default authSlice.reducer;