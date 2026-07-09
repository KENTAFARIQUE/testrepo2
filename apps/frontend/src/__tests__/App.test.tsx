import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../App";

vi.mock("../api/client", () => ({
  getVideo: vi.fn().mockReturnValue(new Promise(() => {})),
  listVideos: vi.fn().mockResolvedValue([]),
  createVideo: vi.fn(),
}));

describe("App", () => {
  it("renders without crashing", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByText("TubeDigest")).toBeTruthy();
  });

  it("renders HomePage on /", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByText("Submit a YouTube Video")).toBeTruthy();
  });

  it("renders JobDetailPage on /jobs/:id", () => {
    render(
      <MemoryRouter initialEntries={["/jobs/123"]}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByText("Loading job details...")).toBeTruthy();
  });
});
