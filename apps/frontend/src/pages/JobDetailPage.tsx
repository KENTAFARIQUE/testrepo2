import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getVideo } from "../api/client";
import type { VideoJobResponse } from "../contracts";
import StatusTimeline from "../components/StatusTimeline";
import ResultCard from "../components/ResultCard";

const TERMINAL_STATUSES = ["completed", "failed"];

export default function JobDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [job, setJob] = useState<VideoJobResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchJob = async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getVideo(id);
      setJob(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load job");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJob();
  }, [id]);

  useEffect(() => {
    if (!job || TERMINAL_STATUSES.includes(job.status)) return;

    const interval = setInterval(fetchJob, 5000);
    return () => clearInterval(interval);
  }, [job?.status]);

  if (loading && !job) {
    return (
      <div className="py-12 text-center text-gray-500" role="status">
        Loading job...
      </div>
    );
  }

  if (error && !job) {
    return (
      <div className="py-12 text-center" role="alert">
        <p className="text-red-600">{error}</p>
        <button
          onClick={fetchJob}
          className="mt-2 text-sm text-blue-600 underline hover:text-blue-800"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!job) return null;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-xl font-bold text-gray-900">
          {job.title || job.url}
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          Submitted: {new Date(job.created_at).toLocaleString()}
        </p>
      </div>

      <div>
        <h3 className="mb-4 text-lg font-semibold text-gray-800">Pipeline</h3>
        <StatusTimeline
          status={job.status}
          currentStep={job.current_step}
          error={job.error}
        />
      </div>

      <ResultCard job={job} />
    </div>
  );
}
