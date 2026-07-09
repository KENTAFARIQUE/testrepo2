import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import JobDetailPage from "./JobDetailPage";
import { getVideo } from "../api/client";

vi.mock("../api/client", () => ({
  getVideo: vi.fn(),
}));

const mockQueuedJob = {
  id: "job-1",
  url: "https://youtube.com/watch?v=test",
  title: null,
  status: "queued" as const,
  current_step: "queued",
  tags: [],
  chapters: [],
  created_at: "2026-07-08T14:00:00Z",
  updated_at: "2026-07-08T14:00:00Z",
  error: null,
};

const mockCompletedJob = {
  id: "job-2",
  url: "https://youtube.com/watch?v=done",
  title: "Complete Video",
  status: "completed" as const,
  current_step: "completed",
  tags: ["demo", "test"],
  chapters: [{ start: "00:00", title: "Intro" }],
  transcript: "Hello world",
  summary: "A test video summary",
  video_path: "storage/videos/done.mp4",
  created_at: "2026-07-08T13:00:00Z",
  updated_at: "2026-07-08T13:30:00Z",
  error: null,
};

const mockFailedJob = {
  id: "job-3",
  url: "https://youtube.com/watch?v=bad",
  title: "Failed Video",
  status: "failed" as const,
  current_step: "downloading",
  tags: [],
  chapters: [],
  created_at: "2026-07-08T12:00:00Z",
  updated_at: "2026-07-08T12:05:00Z",
  error: "Error code: 403 - Forbidden",
};

function renderDetail(id: string) {
  return render(
    <MemoryRouter initialEntries={[`/jobs/${id}`]}>
      <Routes>
        <Route path="/jobs/:id" element={<JobDetailPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

describe("JobDetailPage", () => {
  it("shows loading state initially", () => {
    vi.mocked(getVideo).mockReturnValue(new Promise(() => {}));
    renderDetail("job-1");
    expect(screen.getByText("Loading job details...")).toBeTruthy();
  });

  it("renders queued job with pipeline timeline", async () => {
    vi.mocked(getVideo).mockResolvedValue(mockQueuedJob);
    renderDetail("job-1");

    await waitFor(() => {
      expect(screen.getByText("Untitled Video")).toBeTruthy();
    });
    expect(screen.getByText("https://youtube.com/watch?v=test")).toBeTruthy();
    expect(screen.getAllByText("queued")).toHaveLength(2);
    expect(screen.getByText("downloading")).toBeTruthy();
    expect(screen.getByText("downloaded")).toBeTruthy();
    expect(screen.getByText("Pipeline")).toBeTruthy();
  });

  it("renders completed job with summary, transcript, tags, chapters", async () => {
    vi.mocked(getVideo).mockResolvedValue(mockCompletedJob);
    renderDetail("job-2");

    await waitFor(() => {
      expect(screen.getByText("Complete Video")).toBeTruthy();
    });
    expect(screen.getByText("A test video summary")).toBeTruthy();
    expect(screen.getByText("Hello world")).toBeTruthy();
    expect(screen.getByText("demo")).toBeTruthy();
    expect(screen.getByText("test")).toBeTruthy();
    expect(screen.getByText("Intro")).toBeTruthy();
  });

  it("renders failed job with error message", async () => {
    vi.mocked(getVideo).mockResolvedValue(mockFailedJob);
    renderDetail("job-3");

    await waitFor(() => {
      expect(screen.getByText("Failed Video")).toBeTruthy();
    });
    expect(screen.getByText("Error code: 403 - Forbidden")).toBeTruthy();
  });

  it("shows error state on API failure", async () => {
    vi.mocked(getVideo).mockRejectedValue(new Error("Network error"));
    renderDetail("job-1");

    await waitFor(() => {
      expect(screen.getByText("Network error")).toBeTruthy();
    });
  });

  it("shows retry button on error", async () => {
    vi.mocked(getVideo).mockRejectedValue(new Error("Network error"));
    renderDetail("job-1");

    await waitFor(() => {
      expect(screen.getByText("Retry")).toBeTruthy();
    });
  });

  it("renders back link to home", async () => {
    vi.mocked(getVideo).mockResolvedValue(mockQueuedJob);
    renderDetail("job-1");

    await waitFor(() => {
      expect(screen.getByText("Back to jobs")).toBeTruthy();
    });
  });

  it("shows download button when video_path exists", async () => {
    vi.mocked(getVideo).mockResolvedValue(mockCompletedJob);
    renderDetail("job-2");

    await waitFor(() => {
      expect(screen.getByText("Download")).toBeTruthy();
    });

    const link = screen.getByText("Download").closest("a");
    expect(link?.getAttribute("href")).toContain("/api/videos/job-2/download");
  });
});
