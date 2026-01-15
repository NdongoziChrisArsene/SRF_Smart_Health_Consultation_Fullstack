import API from "./api";

export const checkSymptoms = (symptoms) => {
  return API.post("/ai/check-symptoms/", { symptoms });
};

export const getDoctorRecommendations = (data) => {
  return API.post("/ai/recommend-doctors/", data);
};

export const analyzeMedicalReport = (reportData) => {
  return API.post("/ai/analyze-report/", reportData);
};