import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import StatusTimeline from "./StatusTimeline";

describe("StatusTimeline", () => {
  it("renders all pipeline steps", () => {
    render(<StatusTimeline status="queued" currentStep="queued" />);

    expect(screen.getByText("Queued")).toBeTruthy();
    expect(screen.getByText("Downloading")).toBeTruthy();
    expect(screen.getByText("Completed")).toBeTruthy();
  });

  it("highlights current step as blue", () => {
    render(<StatusTimeline status="transcribing" currentStep="transcribing" />);

    const current = screen.getByText("Transcribe");
    expect(current.className).toContain("text-blue");
  });

  it("shows completed steps as green", () => {
    render(
      <StatusTimeline status="transcribing" currentStep="transcribing" />,
    );

    const completed = screen.getByText("Downloading");
    expect(completed.className).toContain("text-green");
  });

  it("shows failed step with error message", () => {
    render(
      <StatusTimeline
        status="failed"
        currentStep="downloading"
        error="Network error"
      />,
    );

    const failed = screen.getByText("Downloading");
    expect(failed.className).toContain("text-red");

    expect(screen.getByText(/Error: Network error/)).toBeTruthy();
  });

  it("shows future steps as gray", () => {
    render(<StatusTimeline status="queued" currentStep="queued" />);

    const future = screen.getByText("Downloading");
    expect(future.className).toContain("text-gray");
  });
});
