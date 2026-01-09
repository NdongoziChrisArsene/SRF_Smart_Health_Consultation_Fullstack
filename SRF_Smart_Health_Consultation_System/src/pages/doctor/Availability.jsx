import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import API from "../../services/api"; // make sure your API instance is configured

export default function Availability() {
  const [availability, setAvailability] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAvailability = async () => {
      try {
        const res = await API.get("doctor/availability/"); // backend endpoint
        setAvailability(res.data);
      } catch (err) {
        console.error("Failed to fetch availability", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAvailability();
  }, []);

  return (
    <>
      <Navbar />

      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-xl font-bold mb-4">Availability Schedule</h1>

        {loading && <p>Loading availability...</p>}

        {!loading && availability.length === 0 && (
          <p className="text-gray-500">No availability set yet.</p>
        )}

        <div className="space-y-4">
          {availability.map((slot) => (
            <div key={slot.id} className="bg-white p-4 shadow rounded">
              <p>
                <strong>Day:</strong> {slot.day_of_week}
              </p>
              <p>
                <strong>Start Time:</strong> {slot.start_time}
              </p>
              <p>
                <strong>End Time:</strong> {slot.end_time}
              </p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}




