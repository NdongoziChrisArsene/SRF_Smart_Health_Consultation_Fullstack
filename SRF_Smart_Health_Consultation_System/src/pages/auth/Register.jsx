import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import toast from "react-hot-toast";
import API from "../../services/api";
import { setCredentials } from "../../redux/authSlice";

export default function Register() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    password_confirm: "",
    role: "patient",
    specialization: "",
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!form.username.trim()) {
      newErrors.username = "Username is required";
    } else if (form.username.length < 3) {
      newErrors.username = "Username must be at least 3 characters";
    }

    if (!form.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!form.password) {
      newErrors.password = "Password is required";
    } else if (form.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    }

    if (!form.password_confirm) {
      newErrors.password_confirm = "Please confirm your password";
    } else if (form.password !== form.password_confirm) {
      newErrors.password_confirm = "Passwords do not match";
    }

    if (form.role === "doctor" && !form.specialization.trim()) {
      newErrors.specialization = "Specialization is required for doctors";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Prepare data for API
      const payload = {
        username: form.username.trim(),
        email: form.email.trim().toLowerCase(),
        password: form.password,
        password_confirm: form.password_confirm,
        role: form.role,
      };

      // Add specialization only for doctors
      if (form.role === "doctor" && form.specialization.trim()) {
        payload.specialization = form.specialization.trim();
      }

      console.log("Sending registration data:", { ...payload, password: "***", password_confirm: "***" });

      const res = await API.post("api/auth/register/", payload);

      // Store credentials in Redux
      dispatch(setCredentials({
        access: res.data.access,
        refresh: res.data.refresh,
        role: res.data.role
      }));

      toast.success("Registration successful!");

      // Redirect based on user role
      setTimeout(() => {
        if (res.data.role === "doctor") {
          navigate("/doctor");
        } else if (res.data.role === "admin") {
          navigate("/admin");
        } else {
          navigate("/patient");
        }
      }, 500);

    } catch (err) {
      console.error("Registration error:", err.response?.data);

      if (err.response?.data) {
        const apiErrors = err.response.data;

        // Handle field-specific errors from backend
        if (typeof apiErrors === "object") {
          const newErrors = {};
          
          Object.keys(apiErrors).forEach(key => {
            if (Array.isArray(apiErrors[key])) {
              newErrors[key] = apiErrors[key][0];
            } else {
              newErrors[key] = apiErrors[key];
            }
          });

          setErrors(newErrors);

          // Show first error in toast
          const firstError = Object.values(newErrors)[0];
          toast.error(firstError || "Registration failed");
        } else {
          toast.error(apiErrors.detail || apiErrors.error || "Registration failed");
        }
      } else {
        toast.error("Registration failed. Please check your connection and try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white px-4 py-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Create Account
          </h1>
          <p className="text-gray-600">
            Join our healthcare platform today
          </p>
        </div>

        <div className="bg-brand-yellow p-8 rounded-xl shadow-lg border border-gray-100">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">
            Register
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Username Field */}
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                placeholder="johndoe"
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  errors.username ? "border-red-500" : "border-gray-300"
                }`}
                value={form.username}
                onChange={handleChange}
                required
              />
              {errors.username && (
                <p className="mt-1 text-sm text-red-600">{errors.username}</p>
              )}
            </div>

            {/* Email Field */}
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Email Address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                placeholder="john@example.com"
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  errors.email ? "border-red-500" : "border-gray-300"
                }`}
                value={form.email}
                onChange={handleChange}
                required
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                placeholder="••••••••"
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  errors.password ? "border-red-500" : "border-gray-300"
                }`}
                value={form.password}
                onChange={handleChange}
                required
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
              <p className="mt-1 text-xs text-gray-500">
                Must be at least 8 characters
              </p>
            </div>

            {/* Confirm Password Field */}
            <div>
              <label
                htmlFor="password_confirm"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Confirm Password
              </label>
              <input
                id="password_confirm"
                name="password_confirm"
                type="password"
                placeholder="••••••••"
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  errors.password_confirm ? "border-red-500" : "border-gray-300"
                }`}
                value={form.password_confirm}
                onChange={handleChange}
                required
              />
              {errors.password_confirm && (
                <p className="mt-1 text-sm text-red-600">{errors.password_confirm}</p>
              )}
            </div>

            {/* Role Selection */}
            <div>
              <label
                htmlFor="role"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Register As
              </label>
              <select
                id="role"
                name="role"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none bg-white"
                value={form.role}
                onChange={handleChange}
              >
                <option value="patient">Patient</option>
                <option value="doctor">Doctor</option>
              </select>
            </div>

            {/* Specialization (for doctors only) */}
            {form.role === "doctor" && (
              <div className="animate-fadeIn">
                <label
                  htmlFor="specialization"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Specialization
                </label>
                <input
                  id="specialization"
                  name="specialization"
                  type="text"
                  placeholder="e.g., Cardiology, Pediatrics"
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                    errors.specialization ? "border-red-500" : "border-gray-300"
                  }`}
                  value={form.specialization}
                  onChange={handleChange}
                  required
                />
                {errors.specialization && (
                  <p className="mt-1 text-sm text-red-600">{errors.specialization}</p>
                )}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-6 btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold py-3 rounded-lg shadow-md hover:shadow-lg transition-all"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creating Account...
                </span>
              ) : (
                "Create Account"
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{" "}
              <Link 
                to="/login" 
                className="text-brand-red hover:text-brand-red-dark font-medium hover:underline transition-colors"
              >
                Sign In
              </Link>
            </p>
          </div>
        </div>

        <p className="text-center text-xs text-gray-500 mt-6">
          By registering, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}