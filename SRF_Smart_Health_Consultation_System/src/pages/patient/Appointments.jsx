import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";
import Loader from "../../components/Loader";
import { getAppointments } from "../../services/patient.service";
import toast from "react-hot-toast";

export default function Appointments() {
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAppointments();
  }, []);

  const loadAppointments = async () => {
    try {
      const res = await getAppointments();
      setAppointments(res.results || res.data || res);
    } catch (err) {
      console.error("Error loading appointments:", err);
      toast.error("Failed to load appointments");
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const styles = {
      pending: "bg-yellow-100 text-yellow-800",
      approved: "bg-green-100 text-green-800",
      completed: "bg-blue-100 text-blue-800",
      cancelled: "bg-red-100 text-red-800",
    };
    return styles[status] || "bg-gray-100 text-gray-800";
  };

  if (loading) {
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
        <div className="max-w-5xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">My Appointments</h1>
              <p className="text-gray-600">View and manage your appointments</p>
            </div>
            <button
              onClick={() => navigate("/patient/book-appointment")}
              className="btn-primary"
            >
              Book New Appointment
            </button>
          </div>

          {appointments.length === 0 ? (
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <h3 className="mt-2 text-lg font-medium text-gray-900">No appointments</h3>
              <p className="mt-1 text-sm text-gray-500">Get started by booking your first appointment.</p>
              <button
                onClick={() => navigate("/patient/book-appointment")}
                className="mt-4 btn-primary"
              >
                Book Appointment
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {appointments.map((apt) => (
                <div key={apt.id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        Dr. {apt.doctor_name}
                      </h3>
                      {apt.doctor_specialization && (
                        <p className="text-sm text-brand-red">{apt.doctor_specialization}</p>
                      )}
                    </div>
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusBadge(apt.status)}`}>
                      {apt.status}
                    </span>
                  </div>
                  
                  <div className="mt-4 grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Date</p>
                      <p className="font-medium">{new Date(apt.date).toLocaleDateString()}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Time</p>
                      <p className="font-medium">{apt.time}</p>
                    </div>
                  </div>
                  
                  {apt.reason_for_visit && (
                    <div className="mt-4">
                      <p className="text-sm text-gray-600">Reason</p>
                      <p className="text-sm">{apt.reason_for_visit}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}