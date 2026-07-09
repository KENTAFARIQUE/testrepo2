import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getVideo } from "../api/client";
import type { VideoJobResponse } from "../contracts";
import StatusBadge from "../components/StatusBadge";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const POLL_INTERVAL = 5000;

const PIPELINE_STEPS = [
  "queued",
  "downloading",
  "downloaded",
  "extracting_audio",
  "generating_thumbnail",
  "transcribing",
  "summarizing",
  "generating_tags",
  "completed",
] as const;

type StepState = "completed" | "current" | "pending" | "failed" | "skipped";

function isTerminal(status: string) {
  return status === "completed" || status === "failed";
}

function getStepState(
  stepIndex: number,
  status: string,
  currentStep: string,
): StepState {
  if (status === "completed") return "completed";

  const currentIdx = PIPELINE_STEPS.indexOf(currentStep as never);

  if (status === "failed") {
    if (stepIndex < currentIdx) return "completed";
    if (stepIndex === currentIdx) return "failed";
    return "skipped";
  }

  if (stepIndex < currentIdx) return "completed";
  if (stepIndex === currentIdx) return "current";
  return "pending";
}

function stepIcon(state: StepState) {
  switch (state) {
    case "completed":
      return (
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100 text-green-600">
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </span>
      );
    case "current":
      return (
        <span className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-blue-500 bg-white">
          <span className="h-3 w-3 rounded-full bg-blue-500" />
        </span>
      );
    case "failed":
      return (
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-red-100 text-red-600">
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </span>
      );
    case "skipped":
      return (
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100 text-gray-400">
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M20 12H4" />
          </svg>
        </span>
      );
    default:
      return (
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100 text-gray-400">
          <span className="h-3 w-3 rounded-full bg-gray-300" />
        </span>
      );
  }
}

function stepLabel(state: StepState, label: string) {
  const base = "ml-3 text-sm font-medium";
  switch (state) {
    case "completed":
      return `${base} text-green-700 line-through`;
    case "current":
      return `${base} text-blue-700`;
    case "failed":
      return `${base} text-red-700`;
    case "skipped":
      return `${base} text-gray-400`;
    default:
      return `${base} text-gray-500`;
  }
}

function stepConnector(state: StepState) {
  const colors: Record<StepState, string> = {
    completed: "bg-green-400",
    current: "bg-blue-300",
    failed: "bg-red-300",
    skipped: "bg-gray-200",
    pending: "bg-gray-200",
  };
  return (
    <div className={`ml-4 mt-0.5 h-6 w-0.5 ${colors[state]}`} />
  );
}

function PipelineTimeline({
  status,
  currentStep,
}: {
  status: string;
  currentStep: string;
}) {
  return (
    <div className="rounded-lg border bg-white p-6 shadow-sm">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-gray-500">
        Pipeline
      </h3>
      <div className="flex flex-col">
        {PIPELINE_STEPS.map((step, i) => {
          const state = getStepState(i, status, currentStep);
          return (
            <div key={step} className="flex items-start">
              <div className="flex flex-col items-center">
                {stepIcon(state)}
                {i < PIPELINE_STEPS.length - 1 && stepConnector(state)}
              </div>
              <div className={stepLabel(state, step)}>
                <span className="capitalize">{step.replace(/_/g, " ")}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ResultsSection({ job }: { job: VideoJobResponse }) {
  const hasResults =
    job.summary || job.transcript || job.tags.length > 0 || job.chapters.length > 0;

  if (!hasResults) {
    if (job.status === "completed") {
      return (
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500">No results available.</p>
        </div>
      );
    }
    if (job.status === "failed") {
      return null;
    }
    return (
      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <p className="text-sm text-gray-500">
          Results will appear here once processing is complete.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {job.summary && (
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">
            Summary
          </h3>
          <p className="whitespace-pre-wrap text-sm text-gray-800">{job.summary}</p>
        </div>
      )}

      {job.transcript && (
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">
            Transcript
          </h3>
          <p className="whitespace-pre-wrap text-sm text-gray-800">{job.transcript}</p>
        </div>
      )}

      {job.tags.length > 0 && (
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">
            Tags
          </h3>
          <div className="flex flex-wrap gap-2">
            {job.tags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {job.chapters.length > 0 && (
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">
            Chapters
          </h3>
          <ul className="divide-y divide-gray-100">
            {job.chapters.map((ch, i) => (
              <li key={i} className="flex gap-3 py-2 text-sm">
                <span className="shrink-0 font-mono text-gray-400">{ch.start}</span>
                <span className="text-gray-800">{ch.title}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default function JobDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [job, setJob] = useState<VideoJobResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [live, setLive] = useState(false);

  async function fetchJob() {
    if (id) {
      try {
        const data = await getVideo(id);
        setJob(data);
        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load job");
        setLoading(false);
      }
    }
  }

  useEffect(() => {
    if (!id) return;

    setLoading(true);
    setError(null);
    setJob(null);
    setLive(false);

    fetchJob();

    const source = new EventSource(`${BASE_URL}/api/videos/${id}/events`);

    source.onopen = () => setLive(true);

    source.onmessage = () => {
      fetchJob();
    };

    source.onerror = () => {
      source.close();
      setLive(false);
    };

    return () => {
      source.close();
      setLive(false);
    };
  }, [id]);

  if (loading) {
    return (
      <div className="py-16 text-center text-gray-500" role="status">
        Loading job details...
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-16 text-center">
        <p className="text-red-600" role="alert">
          {error}
        </p>
        <button
          onClick={fetchJob}
          className="mt-2 text-sm text-blue-600 underline hover:text-blue-800"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="py-16 text-center text-gray-500">Job not found.</div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Link
          to="/"
          className="inline-flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Back to jobs
        </Link>
        {live && (
          <span className="flex items-center gap-1.5 text-xs text-green-600">
            <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
            Live
          </span>
        )}
      </div>

      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <h2 className="truncate text-lg font-semibold text-gray-900">
              {job.title || "Untitled Video"}
            </h2>
            <p className="mt-1 truncate text-sm text-gray-500">
              <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-blue-600"
              >
                {job.url}
              </a>
            </p>
            <p className="mt-2 text-xs text-gray-400">
              Created: {new Date(job.created_at).toLocaleString()}
            </p>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            {job.video_path && (
              <a
                href={`${BASE_URL}/api/videos/${job.id}/download`}
                download
                className="inline-flex items-center gap-1 rounded-md bg-blue-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-blue-700"
              >
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download
              </a>
            )}
            <StatusBadge status={job.status} />
          </div>
        </div>

        {job.error && (
          <div className="mt-4 rounded-md bg-red-50 p-3">
            <p className="text-sm font-medium text-red-800">Error</p>
            <pre className="mt-1 whitespace-pre-wrap text-xs text-red-700">
              {job.error}
            </pre>
          </div>
        )}
      </div>

      <PipelineTimeline status={job.status} currentStep={job.current_step} />

      <ResultsSection job={job} />
    </div>
  );
}
