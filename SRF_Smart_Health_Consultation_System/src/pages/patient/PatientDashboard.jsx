import { useNavigate } from "react-router-dom";

export default function PatientDashboard() {
  const navigate = useNavigate();

  const Card = ({ title, desc, path }) => (
    <div
      onClick={() => navigate(path)}
      className="p-5 bg-brand-yellow shadow rounded cursor-pointer hover:shadow-lg transition"
    >
      <h2 className="font-semibold mb-1">{title}</h2>
      <p className="text-sm text-gray-600">{desc}</p>
    </div>
  );

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Patient Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card
          title="AI Symptom Checker"
          desc="Check symptoms and get AI health advice"
          path="/patient/symptom-checker"
        />
        <Card
          title="Book Appointment"
          desc="Book and manage appointments"
          path="/patient/book-appointment"
        />
        <Card
          title="Medical History"
          desc="View diagnosis and prescriptions"
          path="/patient/medical-history"
        />
        <Card
          title="Recommended Doctors"
          desc="AI-based doctor recommendations"
          path="/patient/recommended-doctors"
        />
      </div>
    </div>
  );
}



