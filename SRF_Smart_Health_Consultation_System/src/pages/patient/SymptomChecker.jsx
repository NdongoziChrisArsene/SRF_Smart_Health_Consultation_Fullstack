import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import Loader from "../../components/Loader";
import { getMedicalHistory } from "../../services/patient.service";

export default function MedicalHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMedicalHistory()
      .then((res) => setHistory(res.data))
      .catch(() => alert("Failed to load medical history"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader />;

  return (
    <>
      <Navbar />

      <div className="p-6">
        <h1 className="text-xl font-bold mb-4">Medical History</h1>

        {history.length === 0 && (
          <p className="text-gray-500">No medical records found.</p>
        )}

        <div className="space-y-4">
          {history.map((record) => (
            <div key={record.id} className="p-4 bg-white shadow rounded">
              <p><strong>Date:</strong> {record.date}</p>
              <p><strong>Diagnosis:</strong> {record.diagnosis}</p>
              <p><strong>Prescription:</strong> {record.prescription}</p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}







