import { useEffect, useState } from "react";
import StatsCard from "../../components/admin/StatsCard";
import AppointmentChart from "../../components/admin/AppointmentChart";
import NotificationBell from "../../components/admin/NotificationBell";
import AIInsights from "../../components/admin/AIInsights";
import { getReports, getAppointmentTrends } from "../../services/admin.service";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [trend, setTrend] = useState([]);

  useEffect(() => {
    getReports().then(res => setStats(res.data));
    getAppointmentTrends().then(res => setTrend(res.data));
  }, []);

  if (!stats) return <p className="p-6">Loading dashboard...</p>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <NotificationBell />
      </div>

      {/* STATS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatsCard title="Patients" value={stats.total_patients} />
        <StatsCard title="Doctors" value={stats.total_doctors} />
        <StatsCard title="Appointments" value={stats.total_appointments} />
      </div>

      {/* CHART */}
      <AppointmentChart data={trend} />

      {/* AI INSIGHTS */}
      <AIInsights stats={stats} />
    </div>
  );
}




