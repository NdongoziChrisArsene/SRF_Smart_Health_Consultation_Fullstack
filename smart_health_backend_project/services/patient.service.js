import API from "./api";

/**
 * Get patient profile
 */
export const getPatientProfile = () => {
  return API.get("/api/patients/profile/");
};

/**
 * Update patient profile
 */
export const updatePatientProfile = (data) => {
  return API.patch("/api/patients/profile/", data);
};

/**
 * Get medical history
 */
export const getMedicalHistory = () => {
  return API.get("/api/reports/");
};

/**
 * Book appointment
 */
export const bookAppointment = (data) => {
  return API.post("/api/appointments/", data);
};

/**
 * Get appointments
 */
export const getAppointments = () => {
  return API.get("/api/appointments/");
};

/**
 * Get recommended doctors
 */
export const getRecommendedDoctors = () => {
  return API.get("/api/doctors/recommendations/");
};

/**
 * Get all doctors
 */
export const getAllDoctors = () => {
  return API.get("/api/doctors/");
};