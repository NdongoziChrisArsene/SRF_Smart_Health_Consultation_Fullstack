import { NavLink, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";
import { logout } from "../redux/authSlice";

export default function Navbar() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const { role, isAuthenticated } = useSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
    setIsMenuOpen(false);
  };

  const handleLinkClick = (path) => {
    navigate(path); // Navigate when clicking a link
    setIsMenuOpen(false);
  };

  return (
    <nav className="bg-white shadow-sm border-b sticky top-0 z-40 mb-6">
      <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">

        {/* LEFT COLUMN: Logo */}
        <div className="flex-1">
          <NavLink to="/" className="font-semibold text-lg text-slate-800 whitespace-nowrap">
            Smart Health Consultation
          </NavLink>
        </div>

        {/* RIGHT COLUMN: Logout + Hamburger Menu */}
        {isAuthenticated && (
          <div className="flex items-center relative w-[220px]">
            {/* Logout */}
            <button
              onClick={handleLogout}
              className="text-sm font-medium text-brand-red hover:underline"
            >
              Logout
            </button>

            {/* Hamburger */}
            <button
              onClick={() => setIsMenuOpen((prev) => !prev)}
              aria-label="Toggle menu"
              className="ml-auto flex flex-col justify-center space-y-1 p-2 rounded-md hover:bg-slate-100"
            >
              <span className="w-5 h-0.5 bg-slate-700"></span>
              <span className="w-5 h-0.5 bg-slate-700"></span>
              <span className="w-5 h-0.5 bg-slate-700"></span>
            </button>

            {/* Dropdown Menu */}
            {isMenuOpen && (
              <div className="absolute right-0 top-full mt-2 bg-white shadow-lg rounded-md p-3 flex flex-col gap-1 border min-w-[180px]">
                {role === "patient" && (
                  <>
                    <button onClick={() => handleLinkClick("/patient")} className="px-3 py-2 rounded-md text-sm hover:bg-slate-100 text-left">Dashboard</button>
                    <button onClick={() => handleLinkClick("/patient/book")} className="px-3 py-2 rounded-md text-sm hover:bg-slate-100 text-left">Book</button>
                    <button onClick={() => handleLinkClick("/patient/symptoms")} className="px-3 py-2 rounded-md text-sm hover:bg-slate-100 text-left">AI Checker</button>
                    <button onClick={() => handleLinkClick("/patient/history")} className="px-3 py-2 rounded-md text-sm hover:bg-slate-100 text-left">Medical History</button>
                  </>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}







