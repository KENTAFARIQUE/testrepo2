import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import StatusBadge from "./StatusBadge";

const statuses = [
  "queued",
  "downloading",
  "downloaded",
  "extracting_audio",
  "generating_thumbnail",
  "transcribing",
  "summarizing",
  "generating_tags",
  "completed",
  "failed",
] as const;

describe("StatusBadge", () => {
  for (const status of statuses) {
    it(`renders ${status} with correct label`, () => {
      render(<StatusBadge status={status} />);
      const label = status.replace(/_/g, " ");
      expect(screen.getByText(label)).toBeTruthy();
    });
  }

  it("renders unknown status gracefully", () => {
    render(<StatusBadge status={"unknown" as any} />);
    expect(screen.getByText("unknown")).toBeTruthy();
  });
});
