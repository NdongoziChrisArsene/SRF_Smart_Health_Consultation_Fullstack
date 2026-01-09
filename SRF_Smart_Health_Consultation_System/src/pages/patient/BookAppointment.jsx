import { useState } from "react";
import Navbar from "../../components/Navbar";
import { bookAppointment } from "../../services/patient.service";

export default function BookAppointment() {
  const [formData, setFormData] = useState({
    doctor: "",
    date: "",
    reason: "",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await bookAppointment(formData);
      alert("Appointment booked successfully");
      setFormData({ doctor: "", date: "", reason: "" });
    } catch {
      alert("Failed to book appointment");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="p-6">
        <h1 className="text-xl font-bold mb-4">Book Appointment</h1>

        <form className="bg-white p-6 rounded shadow max-w-md" onSubmit={handleSubmit}>
          <input
            type="text"
            name="doctor"
            placeholder="Doctor ID"
            className="input mb-3 w-full"
            value={formData.doctor}
            onChange={handleChange}
            required
          />

          <input
            type="date"
            name="date"
            className="input mb-3 w-full"
            value={formData.date}
            onChange={handleChange}
            required
          />

          <textarea
            name="reason"
            placeholder="Reason for visit"
            className="input mb-3 w-full"
            value={formData.reason}
            onChange={handleChange}
            required
          />

          <button className="btn-primary w-full" disabled={loading}>
            {loading ? "Booking..." : "Book Appointment"}
          </button>
        </form>
      </div>
    </>
  );
}





