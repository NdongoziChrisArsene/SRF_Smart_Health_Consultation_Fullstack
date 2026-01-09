import { useState } from "react";
import API from "../../services/api";
import { BASE_URL } from "../../services/config"; // centralized backend URL

const AddDiagnosis = ({ appointmentId, onSaved }) => {
  const [diagnosis, setDiagnosis] = useState("");
  const [notes, setNotes] = useState("");
  const [prescriptions, setPrescriptions] = useState([
    { medicine_name: "", dosage: "", duration: "" },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const addPrescription = () => {
    setPrescriptions((prev) => [
      ...prev,
      { medicine_name: "", dosage: "", duration: "" },
    ]);
  };

  const handleChange = (index, field, value) => {
    setPrescriptions((prev) =>
      prev.map((p, i) =>
        i === index ? { ...p, [field]: value } : p
      )
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return; // prevent double submit

    setError("");
    setSuccess("");

    const filteredPrescriptions = prescriptions.filter(
      (p) =>
        p.medicine_name.trim() &&
        p.dosage.trim() &&
        p.duration.trim()
    );

    if (!diagnosis.trim()) {
      setError("Diagnosis is required.");
      return;
    }

    setLoading(true);
    try {
      await API.post("diagnosis/create/", {
        appointment: appointmentId,
        diagnosis,
        notes,
        prescriptions: filteredPrescriptions,
      });

      setSuccess("Diagnosis & prescriptions saved successfully!");
      setDiagnosis("");
      setNotes("");
      setPrescriptions([{ medicine_name: "", dosage: "", duration: "" }]);

      if (onSaved) onSaved();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Failed to save diagnosis. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4 p-4 border rounded bg-gray-50"
    >
      <h3 className="text-lg font-semibold">Add Diagnosis</h3>

      {error && <p className="text-red-600">{error}</p>}
      {success && <p className="text-green-600">{success}</p>}

      <textarea
        placeholder="Diagnosis"
        value={diagnosis}
        onChange={(e) => setDiagnosis(e.target.value)}
        className="w-full border p-2 rounded"
      />

      <textarea
        placeholder="Notes"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        className="w-full border p-2 rounded"
      />

      <h4 className="font-medium">Prescriptions</h4>

      {prescriptions.map((p, index) => (
        <div
          key={index}
          className="flex flex-col md:flex-row gap-2 mb-2"
        >
          <input
            placeholder="Medicine Name"
            value={p.medicine_name}
            onChange={(e) =>
              handleChange(index, "medicine_name", e.target.value)
            }
            className="border p-2 rounded flex-1"
          />
          <input
            placeholder="Dosage"
            value={p.dosage}
            onChange={(e) =>
              handleChange(index, "dosage", e.target.value)
            }
            className="border p-2 rounded flex-1"
          />
          <input
            placeholder="Duration"
            value={p.duration}
            onChange={(e) =>
              handleChange(index, "duration", e.target.value)
            }
            className="border p-2 rounded flex-1"
          />
        </div>
      ))}

      <button
        type="button"
        onClick={addPrescription}
        className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        ➕ Add Medicine
      </button>

      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
      >
        {loading ? "Saving..." : "Save"}
      </button>
    </form>
  );
};

export default AddDiagnosis;


