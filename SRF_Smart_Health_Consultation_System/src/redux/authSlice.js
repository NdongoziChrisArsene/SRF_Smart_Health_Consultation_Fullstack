import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import API from "../services/api";

/* =======================
   Async Login Action
======================= */
export const loginUser = createAsyncThunk(
  "auth/login",
  async (credentials, { rejectWithValue }) => {
    try {
      const res = await API.post("/auth/login/", credentials);
      return res.data; // { access, refresh, role }
    } catch {
      return rejectWithValue("Invalid email or password");
    }
  }
);

/* =======================
   Initial State
======================= */
const initialState = {
  accessToken: localStorage.getItem("access_token"),
  refreshToken: localStorage.getItem("refresh_token"),
  role: localStorage.getItem("role"),
  isAuthenticated: !!localStorage.getItem("access_token"),
  loading: false,
  error: null,
};

/* =======================
   Slice
======================= */
const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout: (state) => {
      state.accessToken = null;
      state.refreshToken = null;
      state.role = null;
      state.isAuthenticated = false;
      state.error = null;

      localStorage.clear();
    },

    // ✅ NEW: Sync refreshed token into Redux
    updateAccessToken: (state, action) => {
      state.accessToken = action.payload;
      state.isAuthenticated = true;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        const { access, refresh, role } = action.payload;

        state.loading = false;
        state.accessToken = access;
        state.refreshToken = refresh;
        state.role = role;
        state.isAuthenticated = true;

        localStorage.setItem("access_token", access);
        localStorage.setItem("refresh_token", refresh);
        localStorage.setItem("role", role);
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { logout, updateAccessToken } = authSlice.actions;
export default authSlice.reducer;

















