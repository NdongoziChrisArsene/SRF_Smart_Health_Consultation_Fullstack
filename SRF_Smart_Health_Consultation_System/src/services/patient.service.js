// src/services/patient.service.js

import api from "./api";

/* =====================================================
   PATIENT SERVICE
   → All patient-related API calls
===================================================== */

/**
 * Get patient medical history
 * Used in:
 * - MedicalHistory.jsx
 * - SymptomChecker.jsx
 */
export const getMedicalHistory = async () => {
  try {
    const response = await api.get("/patient/medical-history/");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch medical history:", error);
    throw error;
  }
};

/**
 * Book a new appointment
 * Used in:
 * - BookAppointment.jsx
 */
export const bookAppointment = async (appointmentData) => {
  try {
    const response = await api.post("/appointments/book/", appointmentData);
    return response.data;
  } catch (error) {
    console.error("Failed to book appointment:", error);
    throw error;
  }
};

/**
 * Get patient appointments
 */
export const getPatientAppointments = async () => {
  try {
    const response = await api.get("/patient/appointments/");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch appointments:", error);
    throw error;
  }
};
