import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import toast from "react-hot-toast";
import Navbar from "../../components/Navbar";
import Loader from "../../components/Loader";
import { bookAppointment, getAllDoctors } from "../../services/patient.service";

export default function BookAppointment() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const doctorIdFromUrl = searchParams.get('doctor');

  const [doctors, setDoctors] = useState([]);
  const [loadingDoctors, setLoadingDoctors] = useState(true);
  const [formData, setFormData] = useState({
    doctor: doctorIdFromUrl || "",
    date: "",
    time: "",
    reason: "",
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    loadDoctors();
  }, []);

  const loadDoctors = async () => {
    try {
      const res = await getAllDoctors();
      setDoctors(res.data);
    } catch (err) {
      console.error("Error loading doctors:", err);
      toast.error("Failed to load doctors list");
    } finally {
      setLoadingDoctors(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    // Clear error for this field
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.doctor) {
      newErrors.doctor = "Please select a doctor";
    }

    if (!formData.date) {
      newErrors.date = "Date is required";
    } else {
      const selectedDate = new Date(formData.date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      if (selectedDate < today) {
        newErrors.date = "Cannot book appointments in the past";
      }
    }

    if (!formData.time) {
      newErrors.time = "Time is required";
    }

    if (!formData.reason.trim()) {
      newErrors.reason = "Reason for visit is required";
    } else if (formData.reason.trim().length < 10) {
      newErrors.reason = "Please provide more details (at least 10 characters)";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (!validateForm()) {
    return;
  }

  setLoading(true);

  try {
    const payload = {
      doctor: parseInt(formData.doctor),
      date: formData.date,
      time: formData.time,
      reason_for_visit: formData.reason.trim(),
    };

    await bookAppointment(payload);
    
    toast.success("Appointment booked successfully!");
    
    setFormData({ 
      doctor: "", 
      date: "", 
      time: "",
      reason: "" 
    });

    setTimeout(() => {
      navigate("/patient/appointments");
    }, 1500);

  } catch (err) {
    console.error("Booking error:", err);
    
    if (err.response?.data) {
      const apiErrors = err.response.data;
      
      if (typeof apiErrors === "object" && !Array.isArray(apiErrors)) {
        setErrors(apiErrors);
        const firstError = Object.values(apiErrors)[0];
        toast.error(Array.isArray(firstError) ? firstError[0] : firstError);
      } else {
        toast.error(apiErrors.detail || apiErrors.message || "Failed to book appointment");
      }
    } else {
      toast.error("Failed to book appointment. Please try again.");
    }
  } finally {
    setLoading(false);
  }
  };

  // Get minimum date (today)
  const getMinDate = () => {
    const today = new Date();
    return today.toISOString().split('T')[0];
  };

  // Get maximum date (3 months from now)
  const getMaxDate = () => {
    const maxDate = new Date();
    maxDate.setMonth(maxDate.getMonth() + 3);
    return maxDate.toISOString().split('T')[0];
  };

  if (loadingDoctors) {
    return (
      <>
        <Navbar />
        <div className="flex justify-center items-center min-h-screen">
          <Loader />
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-2xl mx-auto">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Book Appointment</h1>
            <p className="text-gray-600">Schedule a consultation with your preferred doctor</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Select Doctor */}
              <div>
                <label 
                  htmlFor="doctor" 
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Select Doctor <span className="text-red-500">*</span>
                </label>
                <select
                  id="doctor"
                  name="doctor"
                  value={formData.doctor}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none bg-white ${
                    errors.doctor ? "border-red-500" : "border-gray-300"
                  }`}
                  required
                  disabled={loading}
                >
                  <option value="">-- Choose a doctor --</option>
                  {doctors.map((doctor) => (
                    <option key={doctor.id} value={doctor.id}>
                      Dr. {doctor.username || doctor.first_name} {doctor.last_name}
                      {doctor.specialization ? ` - ${doctor.specialization}` : ""}
                    </option>
                  ))}
                </select>
                {errors.doctor && (
                  <p className="mt-1 text-sm text-red-600">{errors.doctor}</p>
                )}
              </div>

              {/* Date Selection */}
              <div>
                <label 
                  htmlFor="date" 
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Appointment Date <span className="text-red-500">*</span>
                </label>
                <input
                  id="date"
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleChange}
                  min={getMinDate()}
                  max={getMaxDate()}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                    errors.date ? "border-red-500" : "border-gray-300"
                  }`}
                  required
                  disabled={loading}
                />
                {errors.date && (
                  <p className="mt-1 text-sm text-red-600">{errors.date}</p>
                )}
              </div>

              {/* Time Selection */}
              <div>
                <label 
                  htmlFor="time" 
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Appointment Time <span className="text-red-500">*</span>
                </label>
                <input
                  id="time"
                  type="time"
                  name="time"
                  value={formData.time}
                  onChange={handleChange}
                  min="08:00"
                  max="18:00"
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none ${
                    errors.time ? "border-red-500" : "border-gray-300"
                  }`}
                  required
                  disabled={loading}
                />
                {errors.time && (
                  <p className="mt-1 text-sm text-red-600">{errors.time}</p>
                )}
                <p className="mt-1 text-xs text-gray-500">
                  Available hours: 8:00 AM - 6:00 PM
                </p>
              </div>

              {/* Reason for Visit */}
              <div>
                <label 
                  htmlFor="reason" 
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Reason for Visit <span className="text-red-500">*</span>
                </label>
                <textarea
                  id="reason"
                  name="reason"
                  rows="4"
                  placeholder="Please describe your symptoms or reason for consultation..."
                  value={formData.reason}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none resize-none ${
                    errors.reason ? "border-red-500" : "border-gray-300"
                  }`}
                  required
                  disabled={loading}
                />
                {errors.reason && (
                  <p className="mt-1 text-sm text-red-600">{errors.reason}</p>
                )}
                <p className="mt-1 text-xs text-gray-500">
                  {formData.reason.length}/500 characters
                </p>
              </div>

              {/* Submit Button */}
              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => navigate("/patient")}
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-colors"
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed"
                  disabled={loading}
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Booking...
                    </span>
                  ) : (
                    "Book Appointment"
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Info Box */}
          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">Appointment Guidelines</h3>
                <div className="mt-2 text-sm text-blue-700">
                  <ul className="list-disc list-inside space-y-1">
                    <li>Arrive 10 minutes before your scheduled time</li>
                    <li>Bring any relevant medical documents</li>
                    <li>You'll receive a confirmation email</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}



