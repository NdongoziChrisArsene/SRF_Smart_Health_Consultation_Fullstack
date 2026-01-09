import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import ForgotPassword from "./pages/auth/ForgotPassword";

// ================= PATIENT PAGES =================
import PatientDashboard from "./pages/patient/PatientDashboard";
import BookAppointment from "./pages/patient/BookAppointment";
import MedicalHistory from "./pages/patient/MedicalHistory";
import SymptomChecker from "./pages/patient/SymptomChecker";
import RecommendedDoctors from "./pages/patient/RecommendedDoctors";

// ================= DOCTOR PAGES =================
import DoctorDashboard from "./pages/doctor/Dashboard";
import DoctorAppointments from "./pages/doctor/Appointments";
import DoctorAvailability from "./pages/doctor/Availability";
import DoctorPatientHistory from "./pages/doctor/PatientHistory";

// ================= ADMIN PAGES =================
import AdminDashboard from "./pages/admin/Dashboard";
import ManageAppointments from "./pages/admin/ManageAppointments";
import ManageDoctors from "./pages/admin/ManageDoctors";
import Reports from "./pages/admin/Reports";

export default function App() {
  return (
    <>
      {/* Example Tailwind dark mode div, can be moved anywhere */}
      <div className="p-6 bg-white dark:bg-gray-900 text-black dark:text-white">
        Tailwind Dark Mode Test
      </div>

      <Routes>
        {/* ================= PUBLIC ROUTES ================= */}
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />

        {/* ================= PATIENT ROUTES ================= */}
        <Route element={<ProtectedRoute allowedRoles={["patient"]} />}>
          <Route path="/patient" element={<PatientDashboard />} />
          <Route path="/patient/book" element={<BookAppointment />} />
          <Route path="/patient/history" element={<MedicalHistory />} />
          <Route path="/patient/symptoms" element={<SymptomChecker />} />
          <Route path="/patient/recommendations" element={<RecommendedDoctors />} />
        </Route>

        {/* ================= DOCTOR ROUTES ================= */}
        <Route element={<ProtectedRoute allowedRoles={["doctor"]} />}>
          <Route path="/doctor" element={<DoctorDashboard />} />
          <Route path="/doctor/appointments" element={<DoctorAppointments />} />
          <Route path="/doctor/availability" element={<DoctorAvailability />} />
          <Route path="/doctor/patients" element={<DoctorPatientHistory />} />
        </Route>

        {/* ================= ADMIN ROUTES ================= */}
        <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/appointments" element={<ManageAppointments />} />
          <Route path="/admin/doctors" element={<ManageDoctors />} />
          <Route path="/admin/reports" element={<Reports />} />
        </Route>

        {/* ================= FALLBACK ================= */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </>
  );
}













