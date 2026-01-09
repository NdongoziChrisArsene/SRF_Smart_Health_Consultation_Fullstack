import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import API from "../../services/api";
import AddDiagnosis from "./AddDiagnosis"; 
import { BASE_URL } from "../../services/config";

export default function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

  const loadAppointments = async () => {
    try {
      const res = await API.get("appointments/");
      setAppointments(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load appointments");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAppointments();
  }, []);

  return (
    <>
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-xl font-bold mb-4">Appointments</h1>

        {loading && <p>Loading appointments...</p>}
        {error && <p className="text-red-600">{error}</p>}
        {!loading && appointments.length === 0 && (
          <p className="text-gray-500">No appointments today.</p>
        )}

        <div className="space-y-6">
          {appointments.map((a) => (
            <div key={a.id} className="bg-white p-4 shadow rounded">
              <p><strong>Patient:</strong> {a.patient.username}</p>
              <p><strong>Date:</strong> {new Date(a.date).toLocaleString()}</p>
              <p><strong>Reason:</strong> {a.reason}</p>

              {/* Existing diagnoses */}
              {a.diagnoses && a.diagnoses.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-semibold mb-2">Diagnoses:</h4>
                  {a.diagnoses.map((d) => (
                    <div key={d.id} className="border p-2 rounded mb-2">
                      <p><strong>Diagnosis:</strong> {d.diagnosis}</p>
                      <p><strong>Notes:</strong> {d.notes}</p>
                      <p>
                        <strong>Prescriptions:</strong>{" "}
                        {d.prescriptions.map((p) => (
                          <span key={p.id || Math.random()}>
                            {p.medicine_name} ({p.dosage}, {p.duration}){" "}
                          </span>
                        ))}
                      </p>
                      <a
                        href={`${BASE_URL}/doctors/prescription/pdf/${d.id}/`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline"
                      >
                        Download Prescription PDF
                      </a>
                    </div>
                  ))}
                </div>
              )}

              {/* Add new diagnosis */}
              <div className="mt-4">
                <AddDiagnosis
                  appointmentId={a.id}
                  onSaved={loadAppointments}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}








