// src/services/ai.service.js

import api from "./api";

/* =====================================================
   AI SERVICE
   → Handles symptom checking via backend AI endpoint
===================================================== */

/**
 * checkSymptoms
 * Sends patient's symptoms to the backend AI endpoint
 * and returns recommended doctors or insights.
 *
 * @param {Object} data - The symptom data, e.g. { symptoms: ["fever", "cough"] }
 * @returns {Promise<Object>} - Response data from backend
 */
export const checkSymptoms = async (data) => {
  try {
    const response = await api.post("/ai/check-symptoms/", data);
    return response.data; // e.g., { recommendedDoctors: [...], insights: [...] }
  } catch (error) {
    console.error("AI service error:", error);
    throw error;
  }
};
