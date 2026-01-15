import { useState } from "react";
import Navbar from "../../components/Navbar";
import Loader from "../../components/Loader";
import { checkSymptoms } from "../../services/ai.service";

export default function SymptomChecker() {
  const [symptoms, setSymptoms] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const res = await checkSymptoms(symptoms);
      setResult(res.data);
    } catch (err) {
      console.error("Symptom check error:", err);
      setError(err.response?.data?.error || "AI service unavailable. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl font-bold mb-6 text-gray-800">AI Symptom Checker</h1>

          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <form onSubmit={handleSubmit}>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Describe Your Symptoms
              </label>
              <textarea
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-red focus:border-transparent transition-all outline-none resize-none"
                rows="6"
                placeholder="Please describe your symptoms in detail. For example: 'I have a headache, fever, and sore throat for 2 days...'"
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                required
                disabled={loading}
              />

              {error && (
                <div className="mt-3 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <button 
                type="submit"
                className="mt-4 w-full btn-primary disabled:bg-gray-400 disabled:cursor-not-allowed"
                disabled={loading || !symptoms.trim()}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing Symptoms...
                  </span>
                ) : (
                  "Analyze Symptoms"
                )}
              </button>
            </form>
          </div>

          {loading && (
            <div className="flex justify-center py-8">
              <Loader />
            </div>
          )}

          {result && !loading && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-start mb-4">
                <div className="flex-shrink-0">
                  <svg className="h-6 w-6 text-brand-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">AI Analysis Result</h2>
                </div>
              </div>

              <div className="prose max-w-none">
                {result.analysis && (
                  <div className="mb-4">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Analysis:</h3>
                    <p className="text-gray-700 whitespace-pre-wrap">{result.analysis}</p>
                  </div>
                )}

                {result.summary && (
                  <div className="mb-4">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Summary:</h3>
                    <p className="text-gray-700">{result.summary}</p>
                  </div>
                )}

                {result.recommendations && (
                  <div className="mb-4">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Recommendations:</h3>
                    <p className="text-gray-700 whitespace-pre-wrap">{result.recommendations}</p>
                  </div>
                )}

                {result.suggested_specialization && (
                  <div className="mb-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h3 className="text-lg font-medium text-blue-900 mb-2">Suggested Specialist:</h3>
                    <p className="text-blue-800">{result.suggested_specialization}</p>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-6 border-t border-gray-200">
                <p className="text-sm text-gray-600 italic">
                  ⚠️ Disclaimer: This is an AI-generated analysis and should not replace professional medical advice. 
                  Please consult with a healthcare provider for accurate diagnosis and treatment.
                </p>
              </div>
            </div>
          )}

          {!result && !loading && !error && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-blue-800">How it works</h3>
                  <div className="mt-2 text-sm text-blue-700">
                    <p>Describe your symptoms in detail and our AI will provide an analysis and recommendations. The more specific you are, the better the results.</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}





