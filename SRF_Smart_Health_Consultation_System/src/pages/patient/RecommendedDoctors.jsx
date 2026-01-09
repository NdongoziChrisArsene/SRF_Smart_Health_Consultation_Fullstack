import { useState } from "react";
import Navbar from "../../components/Navbar";
import Loader from "../../components/Loader";
import { checkSymptoms } from "../../services/ai.service";

export default function SymptomChecker() {
  const [symptoms, setSymptoms] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await checkSymptoms(symptoms);
      setResult(res.data);
    } catch {
      alert("AI service unavailable");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="p-6">
        <h1 className="text-xl font-bold mb-4">AI Symptom Checker</h1>

        <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow max-w-md">
          <textarea
            className="input mb-3 w-full"
            placeholder="Describe your symptoms..."
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            required
          />

          <button className="btn-primary w-full" disabled={loading}>
            {loading ? "Analyzing..." : "Check Symptoms"}
          </button>
        </form>

        {loading && <Loader />}

        {result && !loading && (
          <div className="mt-6 bg-white p-4 rounded shadow">
            <h2 className="font-semibold mb-2">AI Result</h2>
            <p>{result.summary}</p>
          </div>
        )}
      </div>
    </>
  );
}



