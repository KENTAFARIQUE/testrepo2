import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import SubmitForm from "./SubmitForm";
import { createVideo } from "../api/client";

vi.mock("../api/client", () => ({
  createVideo: vi.fn(),
}));

function renderForm() {
  return render(
    <MemoryRouter>
      <SubmitForm />
    </MemoryRouter>,
  );
}

describe("SubmitForm", () => {
  it("renders input and button", () => {
    renderForm();
    expect(screen.getByLabelText("YouTube URL")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Submit" })).toBeTruthy();
  });

  it("shows validation error for empty URL", async () => {
    const user = userEvent.setup();
    renderForm();

    await user.click(screen.getByRole("button", { name: "Submit" }));

    expect(screen.getByRole("alert")).toBeTruthy();
  });

  it("calls createVideo and navigates on valid URL", async () => {
    const mockCreateVideo = vi.mocked(createVideo);
    mockCreateVideo.mockResolvedValue({
      id: "job-42",
      url: "https://youtube.com/watch?v=test",
      status: "queued",
      current_step: "queued",
      tags: [],
      chapters: [],
      created_at: "2026-07-07T00:00:00Z",
      updated_at: "2026-07-07T00:00:00Z",
    });

    const user = userEvent.setup();
    renderForm();

    await user.type(screen.getByLabelText("YouTube URL"), "https://youtube.com/watch?v=test");
    await user.click(screen.getByRole("button", { name: "Submit" }));

    expect(mockCreateVideo).toHaveBeenCalledWith("https://youtube.com/watch?v=test");
  });

  it("disables button while loading", async () => {
    const mockCreateVideo = vi.mocked(createVideo);
    mockCreateVideo.mockImplementation(
      () => new Promise(() => {}), // never resolves
    );

    const user = userEvent.setup();
    renderForm();

    await user.type(screen.getByLabelText("YouTube URL"), "https://youtube.com/watch?v=test");
    await user.click(screen.getByRole("button", { name: "Submit" }));

    expect(screen.getByRole("button", { name: "Submitting..." })).toBeTruthy();
  });

  it("shows error message on API failure", async () => {
    const mockCreateVideo = vi.mocked(createVideo);
    mockCreateVideo.mockRejectedValue(new Error("API error"));

    const user = userEvent.setup();
    renderForm();

    await user.type(screen.getByLabelText("YouTube URL"), "https://youtube.com/watch?v=test");
    await user.click(screen.getByRole("button", { name: "Submit" }));

    expect(await screen.findByText("API error")).toBeTruthy();
  });
});
