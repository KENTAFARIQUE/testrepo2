import type { VideoJobResponse } from "../contracts";

interface ResultCardProps {
  job: VideoJobResponse;
}

export default function ResultCard({ job }: ResultCardProps) {
  if (job.status !== "completed") return null;

  return (
    <div className="space-y-6 rounded-md border border-gray-200 bg-white p-6">
      {job.title && (
        <div>
          <h2 className="text-xl font-bold text-gray-900">{job.title}</h2>
        </div>
      )}

      {job.summary && (
        <div>
          <h3 className="mb-2 text-sm font-semibold text-gray-700">Summary</h3>
          <p className="text-sm text-gray-600">{job.summary}</p>
        </div>
      )}

      {job.tags.length > 0 && (
        <div>
          <h3 className="mb-2 text-sm font-semibold text-gray-700">Tags</h3>
          <div className="flex flex-wrap gap-2">
            {job.tags.map((tag, i) => (
              <span
                key={i}
                className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-800"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {job.chapters.length > 0 && (
        <div>
          <h3 className="mb-2 text-sm font-semibold text-gray-700">Chapters</h3>
          <ul className="space-y-1">
            {job.chapters.map((ch, i) => (
              <li key={i} className="text-sm text-gray-600">
                <span className="font-mono text-gray-400">{ch.start}</span>{" "}
                {ch.title}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
