import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Navbar from "../../components/Navbar";
import API from "../../services/api";
import toast from "react-hot-toast";

export default function AddDiagnosis() {
  const navigate = useNavigate();
  const location = useLocation();
  const appointment = location.state?.appointment;

  const [diagnosis, setDiagnosis] = useState("");
  const [notes, setNotes] = useState("");
  const [prescriptions, setPrescriptions] = useState([
    { medicine_name: "", dosage: "", duration: "" }
  ]);
  const [loading, setLoading] = useState(false);

  const handleAddPrescription = () => {
    setPrescriptions([...prescriptions, { medicine_name: "", dosage: "", duration: "" }]);
  };

  const handleRemovePrescription = (index) => {
    if (prescriptions.length > 1) {
      setPrescriptions(prescriptions.filter((_, i) => i !== index));
    }
  };

  const handlePrescriptionChange = (index, field, value) => {
    const updated = [...prescriptions];
    updated[index][field] = value;
    setPrescriptions(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!diagnosis.trim()) {
      toast.error("Please enter a diagnosis");
      return;
    }

    // Filter out empty prescriptions
    const validPrescriptions = prescriptions.filter(
      (p) => p.medicine_name.trim() && p.dosage.trim() && p.duration.trim()
    );

    setLoading(true);
    try {
      await API.post("doctors/diagnosis/create/", {
        appointment: appointment.id,
        diagnosis: diagnosis.trim(),
        notes: notes.trim(),
        prescriptions: validPrescriptions,
      });

      toast.success("Diagnosis created successfully!");
      navigate("/doctor/appointments");
    } catch (err) {
      console.error("Failed to create diagnosis:", err);
      const errorMsg = err.response?.data?.detail || 
                      err.response?.data?.message || 
                      "Failed to create diagnosis";
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  if (!appointment) {
    return (
      <>
        <Navbar />
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            No appointment selected. Please go back to appointments.
          </div>
          <button
            onClick={() => navigate("/doctor/appointments")}
            className="mt-4 px-4 py-2 bg-brand-red text-white rounded hover:bg-red-700"
          >
            Back to Appointments
          </button>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Add Diagnosis</h1>

        {/* Appointment Info */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-lg font-semibold mb-3">Appointment Details</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Patient:</span>
              <p className="text-gray-900">{appointment.patient_name || "Unknown"}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Date:</span>
              <p className="text-gray-900">{appointment.date}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Time:</span>
              <p className="text-gray-900">{appointment.time}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Status:</span>
              <p className="text-gray-900 capitalize">{appointment.status}</p>
            </div>
          </div>
        </div>

        {/* Diagnosis Form */}
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow space-y-6">
          {/* Diagnosis */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Diagnosis *
            </label>
            <textarea
              value={diagnosis}
              onChange={(e) => setDiagnosis(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-red"
              rows="4"
              placeholder="Enter diagnosis..."
              required
            />
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Notes
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-red"
              rows="3"
              placeholder="Enter additional notes..."
            />
          </div>

          {/* Prescriptions */}
          <div>
            <div className="flex justify-between items-center mb-3">
              <label className="block text-sm font-medium text-gray-700">
                Prescriptions
              </label>
              <button
                type="button"
                onClick={handleAddPrescription}
                className="text-sm px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition"
              >
                + Add Prescription
              </button>
            </div>

            <div className="space-y-4">
              {prescriptions.map((prescription, index) => (
                <div
                  key={index}
                  className="p-4 border border-gray-200 rounded-lg bg-gray-50"
                >
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-medium text-gray-700">
                      Prescription {index + 1}
                    </h3>
                    {prescriptions.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemovePrescription(index)}
                        className="text-red-600 hover:text-red-800 text-sm"
                      >
                        Remove
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs font-medium text-gray-600 mb-1">
                        Medicine Name
                      </label>
                      <input
                        type="text"
                        value={prescription.medicine_name}
                        onChange={(e) =>
                          handlePrescriptionChange(index, "medicine_name", e.target.value)
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-brand-red text-sm"
                        placeholder="e.g., Paracetamol"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-600 mb-1">
                        Dosage
                      </label>
                      <input
                        type="text"
                        value={prescription.dosage}
                        onChange={(e) =>
                          handlePrescriptionChange(index, "dosage", e.target.value)
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-brand-red text-sm"
                        placeholder="e.g., 500mg twice daily"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-600 mb-1">
                        Duration
                      </label>
                      <input
                        type="text"
                        value={prescription.duration}
                        onChange={(e) =>
                          handlePrescriptionChange(index, "duration", e.target.value)
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-brand-red text-sm"
                        placeholder="e.g., 5 days"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Submit Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={() => navigate("/doctor/appointments")}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-brand-red text-white rounded-lg hover:bg-red-700 transition disabled:opacity-50"
              disabled={loading}
            >
              {loading ? "Submitting..." : "Submit Diagnosis"}
            </button>
          </div>
        </form>
      </div>
    </>
  );
}