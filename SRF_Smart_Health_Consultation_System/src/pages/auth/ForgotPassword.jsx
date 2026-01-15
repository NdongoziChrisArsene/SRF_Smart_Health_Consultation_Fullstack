import { useState } from "react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";
import API from "../../services/api";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    // Validation
    if (!email.trim()) {
      setError("Email is required");
      return;
    }

    if (!validateEmail(email)) {
      setError("Please enter a valid email address");
      return;
    }

    setLoading(true);

    try {
      await API.post("api/auth/password-reset/", { 
        email: email.trim().toLowerCase() 
      });
      
      setSuccess(true);
      toast.success("Password reset email sent!");
      
      // Clear the form
      setEmail("");
    } catch (err) {
      console.error("Password reset error:", err.response?.data);

      // For security, we show a generic success message even if the email doesn't exist
      // This prevents email enumeration attacks
      setSuccess(true);
      toast.success("If an account exists, a reset link has been sent");
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
            Enter your email to receive a reset link
          </p>
        </div>

        <div className="bg-brand-yellow p-6 rounded-xl shadow-lg border border-gray-100">
          <h2 className="text-xl font-bold mb-4 text-gray-800">
            Forgot Password
          </h2>

          {success && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-3 py-3 rounded-lg mb-4 text-sm">
              <div className="flex items-start">
                <svg className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <div>
                  <p className="font-medium">Check your email</p>
                  <p className="text-xs mt-1">
                    If an account with this email exists, a password reset link has been sent. 
                    Please check your inbox and spam folder.
                  </p>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded-lg mb-3 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label
                htmlFor="email"
                className="block text-xs font-medium text-gray-700 mb-1"
              >
                Email Address
              </label>
              <input
                id="email"
                type="email"
                placeholder="john@example.com"
                className={`w-full px-3 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  error ? "border-red-500" : "border-gray-300"
                }`}
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError("");
                  setSuccess(false);
                }}
                autoComplete="email"
                required
                disabled={loading}
              />
              {error && (
                <p className="mt-1 text-xs text-red-600">{error}</p>
              )}
            </div>

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
                  Sending...
                </span>
              ) : (
                "Send Reset Link"
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
            Link expires in 1 hour • Protected by encryption
          </p>
        </div>
      </div>
    </div>
  );
}