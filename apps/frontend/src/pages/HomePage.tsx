import { useState } from "react";
import SubmitForm from "../components/SubmitForm";
import JobList from "../components/JobList";
import { clearVideos } from "../api/client";

export default function HomePage() {
  const [refreshKey, setRefreshKey] = useState(0);

  async function handleClear() {
    if (!window.confirm("Delete all jobs?")) return;
    try {
      await clearVideos();
      setRefreshKey((k) => k + 1);
    } catch {
      alert("Failed to clear jobs");
    }
  }

  return (
    <div>
      <h2 className="mb-6 text-xl font-semibold text-gray-800">
        Submit a YouTube Video
      </h2>
      <SubmitForm />
      <div className="mt-10">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-800">Jobs</h3>
          <button
            onClick={handleClear}
            className="rounded-md border border-red-300 px-3 py-1 text-xs font-medium text-red-600 hover:bg-red-50"
          >
            Clear DB
          </button>
        </div>
        <JobList refreshKey={refreshKey} />
      </div>
    </div>
  );
}
