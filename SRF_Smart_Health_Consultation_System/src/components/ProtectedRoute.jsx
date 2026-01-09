import { Navigate, Outlet } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function ProtectedRoute({ role }) {
  const { isAuthenticated, userRole, loading } = useAuth();

  // Optional loading state (safe for refresh)
  if (loading) {
    return null; // or <Loader /> if you want
  }

  // Not logged in
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Role-based guard
  if (role && role !== userRole) {
    return <Navigate to="/login" replace />;
  }

  // Authorized
  return <Outlet />;
}















