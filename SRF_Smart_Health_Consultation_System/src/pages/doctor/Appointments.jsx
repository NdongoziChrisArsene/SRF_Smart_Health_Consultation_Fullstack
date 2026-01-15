import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";
import API from "../../services/api";
import toast from "react-hot-toast";

export default function DoctorAppointments() {
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchAppointments = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await API.get("appointments/doctor/appointments/");
      setAppointments(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Failed to fetch appointments:", err);
      const errorMsg = err.response?.data?.detail || "Failed to load appointments";
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const handleAddDiagnosis = (appointment) => {
    navigate("/doctor/add-diagnosis", { state: { appointment } });
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case "confirmed":
        return "bg-green-100 text-green-800 border-green-200";
      case "completed":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "cancelled":
        return "bg-red-100 text-red-800 border-red-200";
      case "pending":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  const canAddDiagnosis = (appointment) => {
    const status = appointment.status?.toLowerCase();
    return (status === "confirmed" || status === "completed") && !appointment.has_diagnosis;
  };

  return (
    <>
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">My Appointments</h1>

        {loading && (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-red"></div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {!loading && appointments.length === 0 && (
          <div className="bg-white p-8 rounded-lg shadow text-center">
            <p className="text-gray-500 text-lg">No appointments scheduled yet.</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {appointments.map((appointment) => (
            <div
              key={appointment.id}
              className="bg-white p-6 shadow-lg rounded-lg border-l-4 border-brand-red hover:shadow-xl transition"
            >
              {/* Status Badge */}
              <div className="flex justify-between items-start mb-4">
                <span
                  className={`px-3 py-1 text-xs font-semibold rounded-full border ${getStatusColor(
                    appointment.status
                  )}`}
                >
                  {appointment.status || "Unknown"}
                </span>
                {appointment.has_diagnosis && (
                  <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                    ✓ Diagnosed
                  </span>
                )}
              </div>

              {/* Patient Info */}
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {appointment.patient_name || "Patient"}
                </h3>
                {appointment.patient_email && (
                  <p className="text-sm text-gray-600">
                    📧 {appointment.patient_email}
                  </p>
                )}
              </div>

              {/* Appointment Details */}
              <div className="space-y-2 mb-4 text-sm text-gray-700">
                <div className="flex items-center">
                  <svg className="w-4 h-4 mr-2 text-brand-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span className="font-medium">Date:</span>
                  <span className="ml-2">{formatDate(appointment.date)}</span>
                </div>
                <div className="flex items-center">
                  <svg className="w-4 h-4 mr-2 text-brand-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="font-medium">Time:</span>
                  <span className="ml-2">{appointment.time}</span>
                </div>
              </div>

              {/* Reason */}
              {appointment.reason && (
                <div className="mb-4 p-3 bg-gray-50 rounded">
                  <p className="text-xs font-medium text-gray-600 mb-1">Reason:</p>
                  <p className="text-sm text-gray-800">{appointment.reason}</p>
                </div>
              )}

              {/* Action Button */}
              {canAddDiagnosis(appointment) ? (
                <button
                  onClick={() => handleAddDiagnosis(appointment)}
                  className="w-full mt-4 px-4 py-2 bg-brand-red text-white rounded-lg hover:bg-red-700 transition font-medium"
                >
                  Add Diagnosis
                </button>
              ) : appointment.has_diagnosis ? (
                <div className="w-full mt-4 px-4 py-2 bg-gray-100 text-gray-600 rounded-lg text-center text-sm">
                  Diagnosis Already Added
                </div>
              ) : (
                <div className="w-full mt-4 px-4 py-2 bg-gray-100 text-gray-500 rounded-lg text-center text-sm">
                  Cannot Add Diagnosis
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}