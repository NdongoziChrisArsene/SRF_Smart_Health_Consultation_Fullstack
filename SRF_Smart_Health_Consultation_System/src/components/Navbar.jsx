import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../redux/authSlice";

export default function Navbar() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  // Redux state
  const { role, isAuthenticated } = useSelector((state) => state.auth);

  // Fallback (important for refresh safety)
  const userRole = role || localStorage.getItem("role");
  const loggedIn = isAuthenticated || !!localStorage.getItem("access_token");

  const handleLogout = () => {
    dispatch(logout()); // clears redux + localStorage
    navigate("/login");
  };

  return (
    <nav className="bg-blue-600 text-white px-6 py-3 flex justify-between">
      <Link to="/" className="font-bold text-lg">
        Smart Health
      </Link>

      {loggedIn && (
        <div className="space-x-4 flex items-center">
          {userRole === "patient" && (
            <>
              <Link to="/patient">Dashboard</Link>
              <Link to="/patient/book">Book</Link>
              <Link to="/patient/symptoms">AI Checker</Link>
            </>
          )}

          {userRole === "doctor" && (
            <>
              <Link to="/doctor">Dashboard</Link>
              <Link to="/doctor/appointments">Appointments</Link>
            </>
          )}

          {userRole === "admin" && (
            <>
              <Link to="/admin">Dashboard</Link>
              <Link to="/admin/doctors">Doctors</Link>
              <Link to="/admin/reports">Reports</Link>
            </>
          )}

          <button
            onClick={handleLogout}
            className="bg-red-500 px-3 py-1 rounded"
          >
            Logout
          </button>
        </div>
      )}
    </nav>
  );
}







