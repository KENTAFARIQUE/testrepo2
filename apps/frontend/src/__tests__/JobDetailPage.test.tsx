import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import JobDetailPage from "../pages/JobDetailPage";
import { getVideo } from "../api/client";

vi.mock("../api/client", () => ({
  getVideo: vi.fn(),
}));

const mockJob = {
  id: "job-1",
  url: "https://youtube.com/watch?v=test",
  title: "Test Video",
  status: "completed" as const,
  current_step: "completed",
  tags: ["tag1"],
  chapters: [{ start: "00:00", title: "Intro" }],
  summary: "Summary text",
  created_at: "2026-07-07T00:00:00Z",
  updated_at: "2026-07-07T00:00:00Z",
};

function renderPage(id = "job-1") {
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
    renderPage();
    expect(screen.getByText("Loading job...")).toBeTruthy();
  });

  it("fetches job by ID and renders details", async () => {
    vi.mocked(getVideo).mockResolvedValue(mockJob);
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("Pipeline")).toBeTruthy();
    });
    expect(screen.getAllByText("Test Video").length).toBe(2);
    expect(screen.getByText("Summary text")).toBeTruthy();
  });

  it("shows error for missing job", async () => {
    vi.mocked(getVideo).mockRejectedValue(new Error("Not found"));
    renderPage("nonexistent");

    await waitFor(() => {
      expect(screen.getByText("Not found")).toBeTruthy();
    });
  });

  it("starts polling interval when job is processing", async () => {
    const setIntervalSpy = vi.spyOn(globalThis, "setInterval");

    const processingJob = { ...mockJob, status: "downloading" as const };
    vi.mocked(getVideo).mockResolvedValue(processingJob);
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("Pipeline")).toBeTruthy();
    });

    expect(setIntervalSpy).toHaveBeenCalledWith(expect.any(Function), 5000);
    setIntervalSpy.mockRestore();
  });

  it("does not start polling interval when job is completed", async () => {
    const setIntervalSpy = vi.spyOn(globalThis, "setInterval");

    vi.mocked(getVideo).mockResolvedValue(mockJob);
    renderPage();

    await waitFor(() => {
      expect(screen.getByText("Pipeline")).toBeTruthy();
    });

    expect(setIntervalSpy).not.toHaveBeenCalledWith(
      expect.any(Function),
      5000,
    );
    setIntervalSpy.mockRestore();
  });
});
