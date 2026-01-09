import api from "./api";

export const getAllAppointments = () =>
  api.get("/admin/appointments/");

export const getAllDoctors = () =>
  api.get("/admin/doctors/");

export const approveDoctor = (doctorId) =>
  api.patch(`/admin/doctors/${doctorId}/approve/`);

export const getReports = () =>
  api.get("/admin/reports/");

// ✅ ADD THIS
export const getAppointmentTrends = () =>
  api.get("/admin/appointments/trends/");


