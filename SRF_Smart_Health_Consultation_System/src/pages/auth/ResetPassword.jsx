import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import toast from "react-hot-toast";
import API from "../../services/api";

export default function ResetPassword() {
  const { token } = useParams();
  const navigate = useNavigate();
  
  const [form, setForm] = useState({
    password: "",
    password_confirm: "",
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
      const payload = {
        token,
        password: form.password,
        password_confirm: form.password_confirm,
      };

      console.log("Attempting password reset with token");

      await API.post("api/auth/password-reset-confirm/", payload);
      
      toast.success("Password reset successfully!");
      
      // Redirect to login after a brief delay
      setTimeout(() => {
        navigate("/login");
      }, 1500);

    } catch (err) {
      console.error("Password reset error:", err.response?.data);

      if (err.response?.data) {
        const apiErrors = err.response.data;

        // Handle field-specific errors
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
          toast.error(firstError || "Failed to reset password");
        } else {
          const errorMsg = apiErrors.detail || apiErrors.error || "Failed to reset password";
          setErrors({ general: errorMsg });
          toast.error(errorMsg);
        }
      } else if (err.request) {
        toast.error("Cannot connect to server. Please check your connection.");
      } else {
        toast.error("Failed to reset password. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white px-4 py-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-4">
          <h1 className="text-2xl font-bold text-gray-800 mb-1">
            Reset Password
          </h1>
          <p className="text-sm text-gray-600">
            Enter your new password
          </p>
        </div>

        <div className="bg-brand-yellow p-6 rounded-xl shadow-lg border border-gray-100">
          <h2 className="text-xl font-bold mb-4 text-gray-800">
            New Password
          </h2>

          {errors.general && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded-lg mb-3 text-sm">
              {errors.general}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-3">
            {/* New Password Field */}
            <div>
              <label
                htmlFor="password"
                className="block text-xs font-medium text-gray-700 mb-1"
              >
                New Password
              </label>
              <input
                id="password"
                type="password"
                name="password"
                placeholder="••••••••"
                className={`w-full px-3 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  errors.password ? "border-red-500" : "border-gray-300"
                }`}
                value={form.password}
                onChange={handleChange}
                autoComplete="new-password"
                required
                disabled={loading}
              />
              {errors.password && (
                <p className="mt-1 text-xs text-red-600">{errors.password}</p>
              )}
              <p className="mt-1 text-xs text-gray-500">
                Must be at least 8 characters
              </p>
            </div>

            {/* Confirm Password Field */}
            <div>
              <label
                htmlFor="password_confirm"
                className="block text-xs font-medium text-gray-700 mb-1"
              >
                Confirm New Password
              </label>
              <input
                id="password_confirm"
                type="password"
                name="password_confirm"
                placeholder="••••••••"
                className={`w-full px-3 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  errors.password_confirm ? "border-red-500" : "border-gray-300"
                }`}
                value={form.password_confirm}
                onChange={handleChange}
                autoComplete="new-password"
                required
                disabled={loading}
              />
              {errors.password_confirm && (
                <p className="mt-1 text-xs text-red-600">{errors.password_confirm}</p>
              )}
            </div>

            {/* Submit Button */}
            <button
              disabled={loading}
              type="submit"
              className="w-full mt-4 btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold py-2.5 text-sm rounded-lg shadow-md hover:shadow-lg transition-all"
            >
              {loading ? (
                <span className="flex items-center justify-center text-sm">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Resetting...
                </span>
              ) : (
                "Reset Password"
              )}
            </button>
          </form>

          <div className="mt-4 text-center">
            <span className="text-xs text-gray-600">
              Remember your password?{" "}
            </span>
            <Link 
              to="/login" 
              className="text-brand-red hover:text-brand-red-dark font-medium hover:underline transition-colors text-xs"
            >
              Sign In
            </Link>
          </div>
        </div>

        <div className="mt-4 text-center">
          <p className="text-xs text-gray-500">
            Protected by industry-standard encryption
          </p>
        </div>
      </div>
    </div>
  );
}