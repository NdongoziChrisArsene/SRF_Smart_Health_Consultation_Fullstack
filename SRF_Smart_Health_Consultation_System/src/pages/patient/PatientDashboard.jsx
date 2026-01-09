import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";

export default function PatientDashboard() {
  const navigate = useNavigate();

  const Card = ({ title, desc, path }) => (
    <div
      onClick={() => navigate(path)}
      className="p-5 bg-white shadow rounded cursor-pointer hover:shadow-lg transition"
    >
      <h2 className="font-semibold mb-1">{title}</h2>
      <p className="text-sm text-gray-600">{desc}</p>
    </div>
  );

  return (
    <>
      <Navbar />

      <div className="p-6">
        <h1 className="text-2xl font-bold mb-6">Patient Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card
            title="AI Symptom Checker"
            desc="Check symptoms and get AI health advice"
            path="/patient/symptoms"
          />
          <Card
            title="Book Appointment"
            desc="Book and manage appointments"
            path="/patient/book"
          />
          <Card
            title="Medical History"
            desc="View diagnosis and prescriptions"
            path="/patient/history"
          />
          <Card
            title="Recommended Doctors"
            desc="AI-based doctor recommendations"
            path="/patient/recommendations"
          />
        </div>
      </div>
    </>
  );
}




