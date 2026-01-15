import { useState } from "react";

export default function NotificationBell() {
  const [open, setOpen] = useState(false);

  const notifications = [
    "New doctor registered",
    "Appointment cancelled",
    "New patient joined"
  ];

  return (
    <div className="relative">
      <button onClick={() => setOpen(!open)} className="text-xl">
        🔔
      </button>

      {open && (
        <div className="absolute right-0 bg-brand-yellow shadow rounded w-64 mt-2">
          {notifications.map((n, i) => (
            <div key={i} className="p-2 border-b text-sm">
              {n}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
