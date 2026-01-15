import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import API from "../../services/api"; 
import { BASE_URL } from "../../services/config";
import toast from "react-hot-toast";

export default function PatientHistory() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadHistory = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await API.get("doctors/diagnosis/doctor/history/");
      setRecords(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Failed to load history:", err);
      const errorMsg = err.response?.data?.detail || "Failed to load diagnosis history";
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = (diagnosisId) => {
    const pdfUrl = `${BASE_URL}/api/doctors/prescription/pdf/${diagnosisId}/`;
    window.open(pdfUrl, "_blank");
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  };

  return (
    <>
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Patient Diagnosis History</h1>

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

        {!loading && records.length === 0 && (
          <div className="bg-white p-8 rounded-lg shadow text-center">
            <p className="text-gray-500 text-lg">No patient records available.</p>
            <p className="text-gray-400 text-sm mt-2">
              Patient diagnosis records will appear here after you create them.
            </p>
          </div>
        )}

        <div className="space-y-6">
          {records.map((record) => (
            <div key={record.id} className="bg-white p-6 shadow-lg rounded-lg border-l-4 border-brand-red">
              {/* Header: Patient Info & Download Button */}
              <div className="border-b pb-4 mb-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Patient: {record.patient_name || "Unknown"}
                    </h3>
                    <div className="mt-2 space-y-1 text-sm text-gray-600">
                      <p>
                        <span className="font-medium">Date:</span> {formatDate(record.created_at)}
                      </p>
                      {record.appointment_date && (
                        <p>
                          <span className="font-medium">Appointment:</span>{" "}
                          {record.appointment_date} at {record.appointment_time}
                        </p>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => handleDownloadPDF(record.id)}
                    className="px-4 py-2 bg-brand-red text-white text-sm rounded-lg hover:bg-red-700 transition flex items-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Download PDF
                  </button>
                </div>
              </div>

              {/* Diagnosis */}
              <div className="mb-4">
                <p className="text-sm font-semibold text-gray-700 mb-2">Diagnosis:</p>
                <p className="text-gray-900 bg-gray-50 p-3 rounded">{record.diagnosis}</p>
              </div>

              {/* Notes */}
              {record.notes && (
                <div className="mb-4">
                  <p className="text-sm font-semibold text-gray-700 mb-2">Notes:</p>
                  <p className="text-gray-900 bg-gray-50 p-3 rounded">{record.notes}</p>
                </div>
              )}

              {/* Prescriptions */}
              {record.prescriptions && record.prescriptions.length > 0 && (
                <div className="mt-4 pt-4 border-t">
                  <p className="text-sm font-semibold text-gray-700 mb-3">
                    Prescriptions ({record.prescriptions.length}):
                  </p>
                  <div className="space-y-3">
                    {record.prescriptions.map((prescription, idx) => (
                      <div 
                        key={prescription.id || idx} 
                        className="bg-gradient-to-r from-gray-50 to-gray-100 p-4 rounded-lg border border-gray-200"
                      >
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                          <div>
                            <span className="font-semibold text-gray-700 block mb-1">
                              💊 Medicine:
                            </span>
                            <p className="text-gray-900">{prescription.medicine_name}</p>
                          </div>
                          <div>
                            <span className="font-semibold text-gray-700 block mb-1">
                              📋 Dosage:
                            </span>
                            <p className="text-gray-900">{prescription.dosage}</p>
                          </div>
                          <div>
                            <span className="font-semibold text-gray-700 block mb-1">
                              ⏱️ Duration:
                            </span>
                            <p className="text-gray-900">{prescription.duration}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {(!record.prescriptions || record.prescriptions.length === 0) && (
                <div className="mt-4 pt-4 border-t">
                  <p className="text-sm text-gray-500 italic">No prescriptions added</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}