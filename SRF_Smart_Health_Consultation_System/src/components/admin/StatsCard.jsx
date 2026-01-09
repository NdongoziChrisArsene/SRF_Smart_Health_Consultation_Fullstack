export default function StatsCard({ title, value }) {
  return (
    <div className="bg-white p-4 shadow rounded">
      <p className="text-gray-500">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}
