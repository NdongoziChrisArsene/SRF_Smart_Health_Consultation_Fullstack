import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";

// Auth pages
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import ForgotPassword from "./pages/auth/ForgotPassword";
import ResetPassword from "./pages/auth/ResetPassword";

// Admin pages
import AdminDashboard from "./pages/admin/Dashboard";
import ManageAppointments from "./pages/admin/ManageAppointments";
import ManageDoctors from "./pages/admin/ManageDoctors";
import Reports from "./pages/admin/Reports";

// Doctor pages
import DoctorDashboard from "./pages/doctor/Dashboard";
import DoctorAppointments from "./pages/doctor/Appointments";
import Availability from "./pages/doctor/Availability";
import PatientHistory from "./pages/doctor/PatientHistory";
import AddDiagnosis from "./pages/doctor/AddDiagnosis";

// Patient pages  
import Appointments from "./pages/patient/Appointment";
import PatientDashboard from "./pages/patient/PatientDashboard";
import BookAppointment from "./pages/patient/BookAppointment";
import MedicalHistory from "./pages/patient/MedicalHistory";
import RecommendedDoctors from "./pages/patient/RecommendedDoctors";
import SymptomChecker from "./pages/patient/SymptomChecker";

function App() {
  const location = useLocation();

  // Pages where Navbar should NOT appear
  const authRoutes = [
    "/login",
    "/register",
    "/forgot-password",
  ];

  const hideNavbar =
    authRoutes.includes(location.pathname) ||
    location.pathname.startsWith("/reset-password");

  return (
    <>
      {!hideNavbar && <Navbar />}

      <Routes>
        {/* Public */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:token" element={<ResetPassword />} />

        {/* Admin */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/manage-appointments"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <ManageAppointments />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/manage-doctors"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <ManageDoctors />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/reports"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <Reports />
            </ProtectedRoute>
          }
        />

        {/* Doctor */}
        <Route
          path="/doctor"
          element={
            <ProtectedRoute allowedRoles={["doctor"]}>
              <DoctorDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/doctor/appointments"
          element={
            <ProtectedRoute allowedRoles={["doctor"]}>
              <DoctorAppointments />
            </ProtectedRoute>
          }
        />
        <Route
          path="/doctor/availability"
          element={
            <ProtectedRoute allowedRoles={["doctor"]}>
              <Availability />
            </ProtectedRoute>
          }
        />
        <Route
          path="/doctor/patient-history"
          element={
            <ProtectedRoute allowedRoles={["doctor"]}>
              <PatientHistory />
            </ProtectedRoute>
          }
        />
        <Route
          path="/doctor/add-diagnosis"
          element={
            <ProtectedRoute allowedRoles={["doctor"]}>
              <AddDiagnosis />
            </ProtectedRoute>
          }
        />

        {/* Patient */}
        <Route
          path="/patient"
          element={
            <ProtectedRoute allowedRoles={["patient"]}>
              <PatientDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/patient/book-appointment"
          element={
            <ProtectedRoute allowedRoles={["patient"]}>
              <BookAppointment />
            </ProtectedRoute>
          }
        />
        <Route
          path="/patient/medical-history"
          element={
            <ProtectedRoute allowedRoles={["patient"]}>
              <MedicalHistory />
            </ProtectedRoute>
          }
        />
        <Route
          path="/patient/recommended-doctors"
          element={
            <ProtectedRoute allowedRoles={["patient"]}>
              <RecommendedDoctors />
            </ProtectedRoute>
          }
        />
        <Route
          path="/patient/symptom-checker"
          element={
            <ProtectedRoute allowedRoles={["patient"]}>
              <SymptomChecker />
            </ProtectedRoute>
          }
        />  
        <Route
          path="/patient/appointments"
          element={
            <ProtectedRoute allowedRoles={["patient"]}>
              <Appointments />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

export default App;






























