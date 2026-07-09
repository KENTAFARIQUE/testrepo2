import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listVideos } from "../api/client";
import type { VideoJobResponse } from "../contracts";
import StatusBadge from "./StatusBadge";

export default function JobList({ refreshKey = 0 }: { refreshKey?: number }) {
  const [jobs, setJobs] = useState<VideoJobResponse[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchJobs() {
    setLoading(true);
    setError(null);
    try {
      const data = await listVideos();
      setJobs(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load jobs");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchJobs();
  }, [refreshKey]);

  if (loading) {
    return (
      <div className="py-8 text-center text-gray-500" role="status">
        Loading jobs...
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-8 text-center">
        <p className="text-red-600" role="alert">
          {error}
        </p>
        <button
          onClick={fetchJobs}
          className="mt-2 text-sm text-blue-600 underline hover:text-blue-800"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!jobs || jobs.length === 0) {
    return (
      <div className="py-8 text-center text-gray-500">
        No jobs yet. Submit a YouTube URL above to get started.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {jobs.map((job) => (
        <Link
          key={job.id}
          to={`/jobs/${job.id}`}
          className="block rounded-md border border-gray-200 bg-white px-4 py-3 shadow-sm transition hover:shadow-md"
        >
          <div className="flex items-center justify-between">
            <span className="truncate text-sm font-medium text-gray-900">
              {job.title || job.url}
            </span>
            <StatusBadge status={job.status} />
          </div>
          <p className="mt-1 text-xs text-gray-500">
            {new Date(job.created_at).toLocaleString()}
          </p>
        </Link>
      ))}
    </div>
  );
}
