import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function AppointmentChart({ data }) {
  return (
    <div className="bg-white p-4 shadow rounded">
      <h2 className="font-semibold mb-3">Appointment Trend</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="count" stroke="#2563eb" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
