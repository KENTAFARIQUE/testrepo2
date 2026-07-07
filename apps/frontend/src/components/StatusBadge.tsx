import type { JobStatus } from "../contracts";

const statusColors: Record<JobStatus, string> = {
  queued: "bg-gray-100 text-gray-800",
  downloading: "bg-blue-100 text-blue-800",
  downloaded: "bg-blue-100 text-blue-800",
  extracting_audio: "bg-blue-100 text-blue-800",
  generating_thumbnail: "bg-blue-100 text-blue-800",
  transcribing: "bg-blue-100 text-blue-800",
  summarizing: "bg-blue-100 text-blue-800",
  generating_tags: "bg-blue-100 text-blue-800",
  completed: "bg-green-100 text-green-800",
  failed: "bg-red-100 text-red-800",
};

interface StatusBadgeProps {
  status: JobStatus;
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  const color = statusColors[status] ?? "bg-gray-100 text-gray-800";

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${color}`}
    >
      {status.replace(/_/g, " ")}
    </span>
  );
}
