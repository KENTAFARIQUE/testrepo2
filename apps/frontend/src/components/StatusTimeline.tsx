import type { JobStatus } from "../contracts";

const PIPELINE_STEPS: { key: string; label: string }[] = [
  { key: "queued", label: "Queued" },
  { key: "downloading", label: "Downloading" },
  { key: "downloaded", label: "Downloaded" },
  { key: "extracting_audio", label: "Extract Audio" },
  { key: "generating_thumbnail", label: "Thumbnail" },
  { key: "transcribing", label: "Transcribe" },
  { key: "summarizing", label: "Summarize" },
  { key: "generating_tags", label: "Generate Tags" },
  { key: "completed", label: "Completed" },
];

interface StatusTimelineProps {
  status: JobStatus;
  currentStep: string;
  error?: string | null;
}

function stepIndex(step: string): number {
  return PIPELINE_STEPS.findIndex((s) => s.key === step);
}

export default function StatusTimeline({
  status,
  currentStep,
  error,
}: StatusTimelineProps) {
  const currentIdx = stepIndex(currentStep);
  const isFailed = status === "failed";

  return (
    <div className="space-y-2">
      {PIPELINE_STEPS.map((step, idx) => {
        let stateClass = "border-gray-300 text-gray-400";
        let dotClass = "bg-gray-300";

        if (isFailed && idx === currentIdx) {
          stateClass = "border-red-500 text-red-700";
          dotClass = "bg-red-500";
        } else if (idx < currentIdx || (isFailed && idx < currentIdx)) {
          stateClass = "border-green-500 text-green-700";
          dotClass = "bg-green-500";
        } else if (idx === currentIdx) {
          stateClass = "border-blue-500 text-blue-700";
          dotClass = "bg-blue-500";
        }

        return (
          <div key={step.key} className="flex items-center gap-3">
            <div
              className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full ${dotClass}`}
            >
              <span className="text-xs font-bold text-white">
                {idx < currentIdx ? "✓" : idx + 1}
              </span>
            </div>
            <span className={`text-sm font-medium ${stateClass}`}>
              {step.label}
            </span>
          </div>
        );
      })}
      {isFailed && error && (
        <div className="ml-9 mt-2 text-sm text-red-600" role="alert">
          Error: {error}
        </div>
      )}
    </div>
  );
}
