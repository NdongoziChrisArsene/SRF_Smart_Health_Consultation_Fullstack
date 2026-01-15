import API from "./api";

export const getPatientProfile = () => {
  return API.get("/patients/profile/");
};

export const updatePatientProfile = (data) => {
  return API.patch("/patients/profile/", data);
};

export const getMedicalHistory = () => {
  return API.get("/reports/");
};

export const bookAppointment = (data) => {
  return API.post("/appointments/patient/create/", data);
};

export const getAppointments = () => {
  return API.get("/appointments/patient/list/");
};

export const getRecommendedDoctors = () => {
  return API.get("/doctors/recommendations/");
};

export const getAllDoctors = () => {
  return API.get("/doctors/");
};