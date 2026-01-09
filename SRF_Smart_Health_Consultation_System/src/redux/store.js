import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./authSlice";
import { injectStore } from "../services/authSync";

export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
});

// 🔗 Inject Redux store into Axios helpers
injectStore(store);





