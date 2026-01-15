import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import API from "../../services/api";
import toast from "react-hot-toast";

export default function Availability() {
  const [availability, setAvailability] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchAvailability = async () => {
    setLoading(true);
    setError("");
    try {
      // ✅ Fixed: Use correct endpoint
      const res = await API.get("doctors/availability/");
      setAvailability(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Failed to fetch availability:", err);
      const errorMsg = err.response?.data?.detail || "Failed to load availability";
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAvailability();
  }, []);

  const getDayOrder = (day) => {
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    return days.indexOf(day);
  };

  const sortedAvailability = [...availability].sort((a, b) => {
    return getDayOrder(a.day_of_week) - getDayOrder(b.day_of_week);
  });

  return (
    <>
      <Navbar />

      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">My Availability Schedule</h1>

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

        {!loading && availability.length === 0 && (
          <div className="bg-white p-8 rounded-lg shadow text-center">
            <p className="text-gray-500 text-lg">No availability set yet.</p>
            <p className="text-gray-400 text-sm mt-2">
              Contact admin to set up your availability schedule
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sortedAvailability.map((slot) => (
            <div 
              key={slot.id} 
              className="bg-white p-6 shadow-lg rounded-lg border-l-4 border-brand-red hover:shadow-xl transition"
            >
              <h3 className="font-bold text-lg text-gray-900 mb-3">
                {slot.day_of_week}
              </h3>
              <div className="space-y-2">
                <div className="flex items-center text-gray-700">
                  <svg className="h-5 w-5 mr-2 text-brand-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="font-medium">Start:</span>
                  <span className="ml-2">{slot.start_time}</span>
                </div>
                <div className="flex items-center text-gray-700">
                  <svg className="h-5 w-5 mr-2 text-brand-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="font-medium">End:</span>
                  <span className="ml-2">{slot.end_time}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

