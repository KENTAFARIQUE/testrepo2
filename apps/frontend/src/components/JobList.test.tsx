import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import JobList from "./JobList";
import { listVideos } from "../api/client";

vi.mock("../api/client", () => ({
  listVideos: vi.fn(),
}));

const mockJob = {
  id: "job-1",
  url: "https://youtube.com/watch?v=test",
  title: "Test Video",
  status: "queued" as const,
  current_step: "queued",
  tags: [],
  chapters: [],
  created_at: "2026-07-07T00:00:00Z",
  updated_at: "2026-07-07T00:00:00Z",
};

function renderList() {
  return render(
    <MemoryRouter>
      <JobList />
    </MemoryRouter>,
  );
}

describe("JobList", () => {
  it("shows loading state initially", () => {
    vi.mocked(listVideos).mockReturnValue(new Promise(() => {}));
    renderList();
    expect(screen.getByText("Loading jobs...")).toBeTruthy();
  });

  it("renders job rows from mocked API", async () => {
    vi.mocked(listVideos).mockResolvedValue([mockJob]);
    renderList();

    await waitFor(() => {
      expect(screen.getByText("Test Video")).toBeTruthy();
    });
    expect(screen.getByText("queued")).toBeTruthy();
  });

  it("shows empty state when list is empty", async () => {
    vi.mocked(listVideos).mockResolvedValue([]);
    renderList();

    await waitFor(() => {
      expect(
        screen.getByText(/No jobs yet/),
      ).toBeTruthy();
    });
  });

  it("shows error state on API failure", async () => {
    vi.mocked(listVideos).mockRejectedValue(new Error("Network error"));
    renderList();

    await waitFor(() => {
      expect(screen.getByText("Network error")).toBeTruthy();
    });
  });

  it("shows retry button on error", async () => {
    vi.mocked(listVideos).mockRejectedValue(new Error("Network error"));
    renderList();

    await waitFor(() => {
      expect(screen.getByText("Retry")).toBeTruthy();
    });
  });

  it("links to job detail page", async () => {
    vi.mocked(listVideos).mockResolvedValue([mockJob]);
    renderList();

    await waitFor(() => {
      const link = screen.getByRole("link");
      expect(link.getAttribute("href")).toBe("/jobs/job-1");
    });
  });
});
