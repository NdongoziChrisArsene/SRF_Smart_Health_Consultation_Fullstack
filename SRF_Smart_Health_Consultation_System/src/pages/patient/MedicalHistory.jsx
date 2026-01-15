import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import Loader from "../../components/Loader";
import { getMedicalHistory } from "../../services/patient.service";

export default function MedicalHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const res = await getMedicalHistory();
      setHistory(res.data);
    } catch (err) {
      console.error("Error loading medical history:", err);
      setError("Failed to load medical history. Please try again later.");
    } finally {
      setLoading(false);
    }
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
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Medical History</h1>
            <p className="text-gray-600">View your past diagnoses, prescriptions, and medical reports</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {history.length === 0 && !error && (
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 className="mt-2 text-lg font-medium text-gray-900">No medical records found</h3>
              <p className="mt-1 text-sm text-gray-500">Your medical history will appear here after consultations.</p>
            </div>
          )}

          <div className="space-y-4">
            {history.map((record) => (
              <div 
                key={record.id} 
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden"
              >
                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {record.diagnosis || "Medical Report"}
                      </h3>
                      <div className="flex items-center mt-1 text-sm text-gray-600">
                        <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        {new Date(record.date || record.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </div>
                    </div>

                    {/* Status Badge */}
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                      record.status === 'completed' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {record.status || 'Completed'}
                    </span>
                  </div>

                  {/* Doctor Info */}
                  {record.doctor && (
                    <div className="flex items-center mb-4 pb-4 border-b border-gray-200">
                      <svg className="h-5 w-5 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span className="text-sm text-gray-700">
                        Dr. {record.doctor_name || record.doctor}
                      </span>
                    </div>
                  )}

                  {/* Medical Details */}
                  <div className="space-y-3">
                    {record.symptoms && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-1">Symptoms:</h4>
                        <p className="text-sm text-gray-600">{record.symptoms}</p>
                      </div>
                    )}

                    {record.diagnosis && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-1">Diagnosis:</h4>
                        <p className="text-sm text-gray-600">{record.diagnosis}</p>
                      </div>
                    )}

                    {record.prescription && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-1">Prescription:</h4>
                        <p className="text-sm text-gray-600 whitespace-pre-wrap">{record.prescription}</p>
                      </div>
                    )}

                    {record.notes && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-1">Additional Notes:</h4>
                        <p className="text-sm text-gray-600">{record.notes}</p>
                      </div>
                    )}

                    {record.follow_up_date && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <div className="flex items-center text-sm text-gray-600">
                          <svg className="h-4 w-4 mr-2 text-brand-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span className="font-medium">Follow-up:</span>
                          <span className="ml-1">
                            {new Date(record.follow_up_date).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric'
                            })}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  {record.report_file && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <a
                        href={record.report_file}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-brand-red hover:text-brand-red-dark font-medium"
                      >
                        <svg className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Download Report
                      </a>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}

