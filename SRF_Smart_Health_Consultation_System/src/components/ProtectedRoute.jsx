import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";

export default function ProtectedRoute({ allowedRoles }) {
  const { isAuthenticated, role: userRole } = useSelector((state) => state.auth);

  // Not logged in
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Role-based guard
  if (allowedRoles && !allowedRoles.includes(userRole)) {
    return <Navigate to="/login" replace />;
  }

  // Authorized
  return <Outlet />;
}
