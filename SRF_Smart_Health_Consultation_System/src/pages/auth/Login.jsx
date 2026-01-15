import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import toast from "react-hot-toast";
import API from "../../services/api";
import { setCredentials } from "../../redux/authSlice";

export default function Login() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  const [form, setForm] = useState({
    email: "",
    password: "",
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

    if (!form.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!form.password) {
      newErrors.password = "Password is required";
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
        email: form.email.trim().toLowerCase(),
        password: form.password,
      };

      console.log("Attempting login for:", payload.email);

      const res = await API.post("api/auth/login/", payload);

      // Store credentials in Redux
      dispatch(setCredentials({
        access: res.data.access,
        refresh: res.data.refresh,
        role: res.data.role
      }));

      toast.success("Login successful!");

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
      console.error("Login error:", err.response?.data);

      if (err.response?.status === 401) {
        setErrors({ 
          email: "Invalid email or password",
          password: "Invalid email or password"
        });
        toast.error("Invalid email or password");
      } else if (err.response?.data) {
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
          toast.error(firstError || "Login failed");
        } else {
          toast.error(apiErrors.detail || apiErrors.error || "Login failed");
        }
      } else if (err.request) {
        toast.error("Cannot connect to server. Please check your connection.");
      } else {
        toast.error("Login failed. Please try again.");
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
            Welcome Back
          </h1>
          <p className="text-sm text-gray-600">
            Sign in to access your account
          </p>
        </div>

        <div className="bg-brand-yellow p-6 rounded-xl shadow-lg border border-gray-100">
          <h2 className="text-xl font-bold mb-4 text-gray-800">
            Login
          </h2>

          <form onSubmit={handleSubmit} className="space-y-3">
            {/* Email Field */}
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
                name="email"
                placeholder="john@example.com"
                className={`w-full px-3 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  errors.email ? "border-red-500" : "border-gray-300"
                }`}
                value={form.email}
                onChange={handleChange}
                autoComplete="email"
                required
              />
              {errors.email && (
                <p className="mt-1 text-xs text-red-600">{errors.email}</p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label
                htmlFor="password"
                className="block text-xs font-medium text-gray-700 mb-1"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                name="password"
                placeholder="••••••••"
                className={`w-full px-3 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                  errors.password ? "border-red-500" : "border-gray-300"
                }`}
                value={form.password}
                onChange={handleChange}
                autoComplete="current-password"
                required
              />
              {errors.password && (
                <p className="mt-1 text-xs text-red-600">{errors.password}</p>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-4 btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold py-2.5 text-sm rounded-lg shadow-md hover:shadow-lg transition-all"
            >
              {loading ? (
                <span className="flex items-center justify-center text-sm">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Logging in...
                </span>
              ) : (
                "Sign In"
              )}
            </button>
          </form>

          <div className="mt-4 text-center space-y-2">
            <div>
              <Link 
                to="/forgot-password" 
                className="text-brand-red hover:text-brand-red-dark font-medium hover:underline transition-colors text-xs"
              >
                Forgot password?
              </Link>
            </div>

            <div className="pt-1.5 border-t border-gray-200">
              <span className="text-xs text-gray-600">
                Don't have an account?{" "}
              </span>
              <Link 
                to="/register" 
                className="text-brand-red hover:text-brand-red-dark font-medium hover:underline transition-colors text-xs"
              >
                Create an account
              </Link>
            </div>
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















































































































































































































// import { useState } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import { useDispatch } from "react-redux";
// import toast from "react-hot-toast";
// import API from "../../services/api";
// import { setCredentials } from "../../redux/authSlice";

// export default function Login() {
//   const navigate = useNavigate();
//   const dispatch = useDispatch();
  
//   const [form, setForm] = useState({
//     email: "",
//     password: "",
//   });
//   const [loading, setLoading] = useState(false);
//   const [errors, setErrors] = useState({});

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setForm({ ...form, [name]: value });
//     // Clear error for this field when user starts typing
//     if (errors[name]) {
//       setErrors({ ...errors, [name]: "" });
//     }
//   };

//   const validateForm = () => {
//     const newErrors = {};

//     if (!form.email.trim()) {
//       newErrors.email = "Email is required";
//     } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
//       newErrors.email = "Please enter a valid email";
//     }

//     if (!form.password) {
//       newErrors.password = "Password is required";
//     }

//     setErrors(newErrors);
//     return Object.keys(newErrors).length === 0;
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setErrors({});

//     if (!validateForm()) {
//       return;
//     }

//     setLoading(true);

//     try {
//       const payload = {
//         email: form.email.trim().toLowerCase(),
//         password: form.password,
//       };

//       console.log("Attempting login for:", payload.email);

//       const res = await API.post("api/auth/login/", payload);

//       // Store credentials in Redux
//       dispatch(setCredentials({
//         access: res.data.access,
//         refresh: res.data.refresh,
//         role: res.data.role
//       }));

//       toast.success("Login successful!");

//       // Redirect based on user role
//       setTimeout(() => {
//         if (res.data.role === "doctor") {
//           navigate("/doctor");
//         } else if (res.data.role === "admin") {
//           navigate("/admin");
//         } else {
//           navigate("/patient");
//         }
//       }, 500);

//     } catch (err) {
//       console.error("Login error:", err.response?.data);

//       if (err.response?.status === 401) {
//         setErrors({ 
//           email: "Invalid email or password",
//           password: "Invalid email or password"
//         });
//         toast.error("Invalid email or password");
//       } else if (err.response?.data) {
//         const apiErrors = err.response.data;

//         // Handle field-specific errors
//         if (typeof apiErrors === "object") {
//           const newErrors = {};
          
//           Object.keys(apiErrors).forEach(key => {
//             if (Array.isArray(apiErrors[key])) {
//               newErrors[key] = apiErrors[key][0];
//             } else {
//               newErrors[key] = apiErrors[key];
//             }
//           });

//           setErrors(newErrors);

//           // Show first error in toast
//           const firstError = Object.values(newErrors)[0];
//           toast.error(firstError || "Login failed");
//         } else {
//           toast.error(apiErrors.detail || apiErrors.error || "Login failed");
//         }
//       } else if (err.request) {
//         toast.error("Cannot connect to server. Please check your connection.");
//       } else {
//         toast.error("Login failed. Please try again.");
//       }
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-white px-4 py-8">
//       <div className="w-full max-w-md">
//         <div className="text-center mb-4">
//           <h1 className="text-2xl font-bold text-gray-800 mb-1">
//             Welcome Back
//           </h1>
//           <p className="text-sm text-gray-600">
//             Sign in to access your account
//           </p>
//         </div>

//         <div className="bg-brand-yellow p-6 rounded-xl shadow-lg border border-gray-100">
//           <h2 className="text-xl font-bold mb-4 text-gray-800">
//             Login
//           </h2>

//           <form onSubmit={handleSubmit} className="space-y-3">
//             {/* Email Field */}
//             <div>
//               <label
//                 htmlFor="email"
//                 className="block text-xs font-medium text-gray-700 mb-1"
//               >
//                 Email Address
//               </label>
//               <input
//                 id="email"
//                 type="email"
//                 name="email"
//                 placeholder="john@example.com"
//                 className={`w-full px-3 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
//                   errors.email ? "border-red-500" : "border-gray-300"
//                 }`}
//                 value={form.email}
//                 onChange={handleChange}
//                 autoComplete="email"
//                 required
//               />
//               {errors.email && (
//                 <p className="mt-1 text-xs text-red-600">{errors.email}</p>
//               )}
//             </div>

//             {/* Password Field */}
//             <div>
//               <label
//                 htmlFor="password"
//                 className="block text-xs font-medium text-gray-700 mb-1"
//               >
//                 Password
//               </label>
//               <input
//                 id="password"
//                 type="password"
//                 name="password"
//                 placeholder="••••••••"
//                 className={`w-full px-3 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
//                   errors.password ? "border-red-500" : "border-gray-300"
//                 }`}
//                 value={form.password}
//                 onChange={handleChange}
//                 autoComplete="current-password"
//                 required
//               />
//               {errors.password && (
//                 <p className="mt-1 text-xs text-red-600">{errors.password}</p>
//               )}
//             </div>

//             {/* Submit Button */}
//             <button
//               type="submit"
//               disabled={loading}
//               className="w-full mt-4 btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold py-2.5 text-sm rounded-lg shadow-md hover:shadow-lg transition-all"
//             >
//               {loading ? (
//                 <span className="flex items-center justify-center text-sm">
//                   <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
//                     <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
//                     <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
//                   </svg>
//                   Logging in...
//                 </span>
//               ) : (
//                 "Sign In"
//               )}
//             </button>
//           </form>

//           <div className="mt-4 text-center space-y-2">
//             <div>
//               <Link 
//                 to="/forgot-password" 
//                 className="text-brand-red hover:text-brand-red-dark font-medium hover:underline transition-colors text-xs"
//               >
//                 Forgot password?
//               </Link>
//             </div>

//             <div className="pt-1.5 border-t border-gray-200">
//               <span className="text-xs text-gray-600">
//                 Don't have an account?{" "}
//               </span>
//               <Link 
//                 to="/register" 
//                 className="text-brand-red hover:text-brand-red-dark font-medium hover:underline transition-colors text-xs"
//               >
//                 Create an account
//               </Link>
//             </div>
//           </div>
//         </div>

//         <div className="mt-4 text-center">
//           <p className="text-xs text-gray-500">
//             Protected by industry-standard encryption
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// } 
