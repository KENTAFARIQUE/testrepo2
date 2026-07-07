import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import ResultCard from "./ResultCard";

const completedJob = {
  id: "job-1",
  url: "https://youtube.com/watch?v=test",
  title: "Test Video",
  status: "completed" as const,
  current_step: "completed",
  tags: ["tag1", "tag2"],
  chapters: [{ start: "00:00", title: "Intro" }],
  summary: "A great video summary",
  created_at: "2026-07-07T00:00:00Z",
  updated_at: "2026-07-07T00:00:00Z",
};

const processingJob = {
  ...completedJob,
  status: "downloading" as const,
  current_step: "downloading",
};

describe("ResultCard", () => {
  it("renders title, summary, tags, chapters when completed", () => {
    render(<ResultCard job={completedJob} />);

    expect(screen.getByText("Test Video")).toBeTruthy();
    expect(screen.getByText("A great video summary")).toBeTruthy();
    expect(screen.getByText("tag1")).toBeTruthy();
    expect(screen.getByText("tag2")).toBeTruthy();
    expect(screen.getByText("Intro")).toBeTruthy();
    expect(screen.getByText("00:00")).toBeTruthy();
  });

  it("returns null when job is not completed", () => {
    const { container } = render(<ResultCard job={processingJob} />);

    expect(container.innerHTML).toBe("");
  });
});
