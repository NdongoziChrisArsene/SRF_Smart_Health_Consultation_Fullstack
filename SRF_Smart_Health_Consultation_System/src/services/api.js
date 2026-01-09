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
    if (token) {
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


















































































































































// import axios from "axios";
// import { BASE_URL } from "./config";

// /* =====================================================
//    Axios instance
// ===================================================== */

// const API = axios.create({
//   baseURL: BASE_URL,
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// /* =====================================================
//    REQUEST INTERCEPTOR
//    → Attach access token automatically
// ===================================================== */

// API.interceptors.request.use(
//   (config) => {
//     const token = localStorage.getItem("access_token");
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
//   },
//   (error) => Promise.reject(error)
// );

// /* =====================================================
//    RESPONSE INTERCEPTOR
//    → Handle 401 + Refresh Token Logic
// ===================================================== */

// let isRefreshing = false;
// let failedQueue = [];

// const processQueue = (error, token = null) => {
//   failedQueue.forEach((prom) => {
//     if (error) {
//       prom.reject(error);
//     } else {
//       prom.resolve(token);
//     }
//   });
//   failedQueue = [];
// };

// API.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const originalRequest = error.config;

//     // If unauthorized and not already retried
//     if (
//       error.response?.status === 401 &&
//       !originalRequest._retry
//     ) {
//       originalRequest._retry = true;

//       const refreshToken = localStorage.getItem("refresh_token");

//       // No refresh token → logout
//       if (!refreshToken) {
//         logoutUser();
//         return Promise.reject(error);
//       }

//       // If already refreshing → queue request
//       if (isRefreshing) {
//         return new Promise((resolve, reject) => {
//           failedQueue.push({ resolve, reject });
//         })
//           .then((token) => {
//             originalRequest.headers.Authorization = `Bearer ${token}`;
//             return API(originalRequest);
//           })
//           .catch((err) => Promise.reject(err));
//       }

//       isRefreshing = true;

//       try {
//         const res = await axios.post(
//           `${BASE_URL}/auth/token/refresh/`,
//           { refresh: refreshToken }
//         );

//         const newAccessToken = res.data.access;

//         localStorage.setItem("access_token", newAccessToken);

//         API.defaults.headers.Authorization = `Bearer ${newAccessToken}`;
//         processQueue(null, newAccessToken);

//         return API(originalRequest);
//       } catch (err) {
//         processQueue(err, null);
//         logoutUser();
//         return Promise.reject(err);
//       } finally {
//         isRefreshing = false;
//       }
//     }

//     return Promise.reject(error);
//   }
// );

// /* =====================================================
//    LOGOUT HELPER
// ===================================================== */

// function logoutUser() {
//   localStorage.clear();
//   window.location.href = "/login";
// }

// export default API;

// /* ================= EXISTING FUNCTIONS (UNCHANGED) ================= */

// export const fetchDoctorDiagnosisHistory = async () => {
//   const res = await API.get("/diagnosis/doctor/history/");
//   return res.data;
// };

// export const fetchPatientDiagnosisHistory = async () => {
//   const res = await API.get("/diagnosis/patient/history/");
//   return res.data;
// };

// export const downloadPrescriptionPDF = async (diagnosisId) => {
//   const res = await API.get(`/prescription/pdf/${diagnosisId}/`, {
//     responseType: "blob",
//   });

//   const url = window.URL.createObjectURL(new Blob([res.data]));
//   const link = document.createElement("a");
//   link.href = url;
//   link.setAttribute("download", "prescription.pdf");
//   document.body.appendChild(link);
//   link.click();
//   link.remove();
// };















































































































// import axios from "axios";
// import { BASE_URL } from "./config";

// const API = axios.create({
//   baseURL: BASE_URL,
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// // 🔐 Attach token automatically
// API.interceptors.request.use((config) => {
//   const token = localStorage.getItem("access_token");
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   }
//   return config;
// });

// // 🔁 Handle expired token globally
// API.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response?.status === 401) {
//       localStorage.clear();
//       window.location.href = "/login";
//     }
//     return Promise.reject(error);
//   }
// );

// export default API;

// /* ================= EXISTING FUNCTIONS (UNCHANGED) ================= */

// export const fetchDoctorDiagnosisHistory = async () => {
//   const res = await API.get("/diagnosis/doctor/history/");
//   return res.data;
// };

// export const fetchPatientDiagnosisHistory = async () => {
//   const res = await API.get("/diagnosis/patient/history/");
//   return res.data;
// };

// export const downloadPrescriptionPDF = async (diagnosisId) => {
//   const res = await API.get(`/prescription/pdf/${diagnosisId}/`, {
//     responseType: "blob",
//   });

//   const url = window.URL.createObjectURL(new Blob([res.data]));
//   const link = document.createElement("a");
//   link.href = url;
//   link.setAttribute("download", "prescription.pdf");
//   document.body.appendChild(link);
//   link.click();
//   link.remove();
// };



































































































// import axios from "axios"; 
// import { BASE_URL } from "./config";

// const API_URL = "https://your-backend.onrender.com/"; // replace with your backend URL

// const authHeaders = () => ({
//   Authorization: `Bearer ${localStorage.getItem("access_token")}`,
// });

// const API = axios.create({
//   baseURL: API_URL,
//   headers: { ...authHeaders(), 
//     "Content-Type": "application/json",
//   }, 
// });

// export default API;

// // Doctor Diagnosis History
// export const fetchDoctorDiagnosisHistory = async () => {
//   const res = await API.get("diagnosis/doctor/history/");
//   return res.data;
// };

// // Patient Diagnosis History
// export const fetchPatientDiagnosisHistory = async () => {
//   const res = await API.get("diagnosis/patient/history/");
//   return res.data;
// };

// // Download PDF
// export const downloadPrescriptionPDF = async (diagnosisId) => {
//   const res = await API.get(`prescription/pdf/${diagnosisId}/`, {
//     responseType: "blob",
//   });
//   const url = window.URL.createObjectURL(new Blob([res.data]));
//   const link = document.createElement("a");
//   link.href = url;
//   link.setAttribute("download", "prescription.pdf");
//   document.body.appendChild(link);
//   link.click();
//   link.remove();
// };







































































// import axios from "axios";  

// const api = axios.create({
//     baseURL: "http://127.0.0.1:8000/api",
// }) 

// api.interceptors.request.use((config) => {
//     const token = localStorage.getItem("access"); 
//     if (token) config.headers.Authorization = `Bearer ${token}`
//     return config
// }) 

// export default api