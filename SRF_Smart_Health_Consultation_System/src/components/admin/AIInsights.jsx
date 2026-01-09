export default function AIInsights({ stats }) {
  const insights = [];

  if (stats.total_appointments > 50) {
    insights.push("📈 High appointment load this period");
  }

  if (stats.total_doctors < 5) {
    insights.push("⚠️ Low number of doctors available");
  }

  if (stats.total_patients > 100) {
    insights.push("🧍 Rapid patient growth detected");
  }

  return (
    <div className="bg-white p-4 shadow rounded">
      <h2 className="font-semibold mb-2">AI Insights</h2>
      <ul className="list-disc pl-5 space-y-1">
        {insights.length ? insights.map((i, idx) => (
          <li key={idx}>{i}</li>
        )) : <li>No insights yet</li>}
      </ul>
    </div>
  );
}
