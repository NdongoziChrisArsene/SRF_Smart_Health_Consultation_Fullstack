import { useEffect, useState } from "react";
import { getAllAppointments } from "../../services/admin.service";

export default function ManageAppointments() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAllAppointments()
      .then((res) => setAppointments(res.data))
      .catch(() => alert("Failed to load appointments"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">All Appointments</h1>

      {loading && <p>Loading...</p>}

      {!loading && appointments.length === 0 && (
        <p className="text-gray-500">No appointments found.</p>
      )}

      <div className="space-y-4">
        {appointments.map((a) => (
          <div key={a.id} className="bg-white p-4 shadow rounded">
            <p><strong>Patient:</strong> {a.patient_name}</p>
            <p><strong>Doctor:</strong> {a.doctor_name}</p>
            <p><strong>Date:</strong> {a.date}</p>
            <p><strong>Status:</strong> {a.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
}




