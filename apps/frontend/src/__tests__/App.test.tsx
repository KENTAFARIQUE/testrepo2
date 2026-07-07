import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../App";

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
    expect(screen.getByText(/Job Detail Page/)).toBeTruthy();
  });
});
