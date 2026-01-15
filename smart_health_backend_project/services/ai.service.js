import API from "./api";

/**
 * Check symptoms using AI
 */
export const checkSymptoms = (symptoms) => {
  return API.post("/api/ai/check-symptoms/", { symptoms });
};

/**
 * Get doctor recommendations based on symptoms
 */
export const getDoctorRecommendations = (symptoms) => {
  return API.post("/api/ai/recommend-doctors/", { symptoms });
};

/**
 * Analyze medical report
 */
export const analyzeMedicalReport = (reportData) => {
  return API.post("/api/ai/analyze-report/", reportData);
};  