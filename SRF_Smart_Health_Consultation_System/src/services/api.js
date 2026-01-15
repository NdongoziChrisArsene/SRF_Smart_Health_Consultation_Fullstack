import axios from "axios";
import { BASE_URL } from "./config";
import { reduxLogout, reduxUpdateAccessToken } from "./authSync"; // NEW

/* =====================================================
   Axios instance
===================================================== */
const API = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/* =====================================================
   REQUEST INTERCEPTOR
   → Attach access token automatically
===================================================== */
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    // Don't add token for auth endpoints
    if (token && !config.url.includes('/auth/')) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/* =====================================================
   RESPONSE INTERCEPTOR
   → Handle 401 + Refresh Token Logic
===================================================== */
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If unauthorized and not already retried
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh_token");

      // No refresh token → logout
      if (!refreshToken) {
        logoutUser();
        return Promise.reject(error);
      }

      // If already refreshing → queue request
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return API(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      isRefreshing = true;

      try {
        const res = await axios.post(
          `${BASE_URL}/auth/token/refresh/`,
          { refresh: refreshToken }
        );

        const newAccessToken = res.data.access;

        // ✅ Update localStorage
        localStorage.setItem("access_token", newAccessToken);

        // ✅ Update default Axios header
        API.defaults.headers.Authorization = `Bearer ${newAccessToken}`;

        // ✅ Update Redux state
        reduxUpdateAccessToken(newAccessToken);

        processQueue(null, newAccessToken);

        return API(originalRequest);
      } catch (err) {
        processQueue(err, null);
        logoutUser();
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

/* =====================================================
   LOGOUT HELPER
   → Use Redux for UI + state sync
===================================================== */
function logoutUser() {
  reduxLogout(); // clears Redux + localStorage
  window.location.href = "/login";
}

export default API;

/* ================= EXISTING FUNCTIONS (UNCHANGED) ================= */
export const fetchDoctorDiagnosisHistory = async () => {
  const res = await API.get("/diagnosis/doctor/history/");
  return res.data;
};

export const fetchPatientDiagnosisHistory = async () => {
  const res = await API.get("/diagnosis/patient/history/");
  return res.data;
};

export const downloadPrescriptionPDF = async (diagnosisId) => {
  const res = await API.get(`/prescription/pdf/${diagnosisId}/`, {
    responseType: "blob",
  });

  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", "prescription.pdf");
  document.body.appendChild(link);
  link.click();
  link.remove();
};

/* =====================================================
   Password reset helper
   - Will call backend endpoint if present
   - Returns the server response, or throws an error
   - UI should show a generic success message even on 4xx to avoid revealing account existence
===================================================== */
export const sendPasswordReset = async (email) => {
  const payload = { email };
  const res = await API.post(`/auth/password/reset/`, payload);
  return res.data;
};































































