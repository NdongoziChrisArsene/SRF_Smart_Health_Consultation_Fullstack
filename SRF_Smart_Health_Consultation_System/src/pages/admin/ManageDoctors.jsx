import { useEffect, useState } from "react";
import { getAllDoctors } from "../../services/admin.service";

export default function ManageDoctors() {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAllDoctors()
      .then(res => setDoctors(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Doctors</h1>

      {loading && <p>Loading...</p>}

      {doctors.map(d => (
        <div key={d.id} className="bg-brand-yellow p-4 shadow rounded mb-2">
          <p><strong>Name:</strong> {d.name}</p>
          <p><strong>Specialty:</strong> {d.specialty}</p>
          <p><strong>Status:</strong> {d.is_active ? "Active" : "Inactive"}</p>
        </div>
      ))}
    </div>
  );
}



