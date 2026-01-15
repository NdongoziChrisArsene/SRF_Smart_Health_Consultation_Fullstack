import { useEffect, useState } from "react";
import { getReports } from "../../services/admin.service";

export default function Reports() {
  const [reports, setReports] = useState(null);

  useEffect(() => {
    getReports()
      .then((res) => setReports(res.data))
      .catch(() => alert("Failed to load reports"));
  }, []);

  if (!reports) return <p className="p-6">Loading reports...</p>;

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">System Reports</h1>

      <div className="bg-brand-yellow p-4 shadow rounded space-y-2">
        <p><strong>Total Patients:</strong> {reports.total_patients}</p>
        <p><strong>Total Doctors:</strong> {reports.total_doctors}</p>
        <p><strong>Total Appointments:</strong> {reports.total_appointments}</p>
      </div>
    </div>
  );
}



