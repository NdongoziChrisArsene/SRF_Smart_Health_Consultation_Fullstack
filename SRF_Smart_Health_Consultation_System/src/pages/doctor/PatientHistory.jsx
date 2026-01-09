import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import API from "../../services/api"; 
import { BASE_URL } from "../../services/config";

export default function PatientHistory() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

  const loadHistory = async () => {
    try {
      const res = await API.get("diagnosis/patient/history/");
      setRecords(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load diagnosis history");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = (diagnosisId) => {
  window.open(`${BASE_URL}/doctors/prescription/pdf/${diagnosisId}/`, "_blank");
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <>
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-xl font-bold mb-4">Patient History</h1>

        {loading && <p>Loading records...</p>}
        {error && <p className="text-red-600">{error}</p>}
        {!loading && records.length === 0 && (
          <p className="text-gray-500">No patient records available.</p>
        )}

        <div className="space-y-4">
          {records.map((r) => (
            <div key={r.id} className="bg-white p-4 shadow rounded">
              <p><strong>Doctor:</strong> {r.appointment.doctor.username}</p>
              <p><strong>Diagnosis:</strong> {r.diagnosis}</p>
              <p><strong>Notes:</strong> {r.notes}</p>

              <div className="mt-2">
                <button
                  className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                  onClick={() => handleDownloadPDF(r.id)}
                >
                  Download Prescription PDF
                </button>
              </div>

              <div className="mt-2">
                {r.prescriptions.map((p) => (
                  <p key={p.id || Math.random()}>
                    <strong>Medicine:</strong> {p.medicine_name},{" "}
                    <strong>Dosage:</strong> {p.dosage},{" "}
                    <strong>Duration:</strong> {p.duration}
                  </p>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}





