import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";

export default function DoctorDashboard() {
  const navigate = useNavigate();

  const Card = ({ title, description, path }) => (
    <div
      onClick={() => navigate(path)}
      className="p-5 bg-white rounded shadow cursor-pointer hover:shadow-lg transition"
    >
      <h2 className="font-semibold text-lg mb-1">{title}</h2>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  );

  return (
    <>
      <Navbar />

      <div className="max-w-6xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Doctor Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card
            title="Appointments"
            description="View today's appointments and add diagnosis"
            path="/doctor/appointments"
          />

          <Card
            title="Availability"
            description="Manage your availability schedule"
            path="/doctor/availability"
          />

          <Card
            title="Patient History"
            description="View patient diagnosis history and download prescriptions"
            path="/doctor/patient-history"
          />
        </div>
      </div>
    </>
  );
}



