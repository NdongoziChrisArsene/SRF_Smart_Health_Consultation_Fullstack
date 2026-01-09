// src/utils/exportUtils.js

/**
 * Convert array of objects to CSV and trigger download
 * @param {Array} data - Array of objects (appointments, users, reports)
 * @param {String} filename - Name of the CSV file
 */
export function exportToCSV(data = [], filename = "export.csv") {
  if (!Array.isArray(data) || data.length === 0) {
    console.warn("exportToCSV: No data provided");
    return;
  }

  // Extract headers from first object
  const headers = Object.keys(data[0]);

  // Build CSV rows
  const csvRows = [
    headers.join(","), // header row
    ...data.map((row) =>
      headers.map((field) => `"${row[field] ?? ""}"`).join(",")
    ),
  ];

  const csvContent = csvRows.join("\n");

  // Create Blob
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  // Create download link
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", filename);

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/**
 * Prepare clean data for PDF generation
 * (PDF rendering handled elsewhere)
 */
export function formatForPDF(data = []) {
  if (!Array.isArray(data)) return [];

  return data.map((item, index) => ({
    index: index + 1,
    ...item,
  }));
}

/**
 * Format date safely (backend-friendly)
 */
export function formatDate(dateString) {
  if (!dateString) return "-";

  const date = new Date(dateString);
  return date.toLocaleDateString();
}




