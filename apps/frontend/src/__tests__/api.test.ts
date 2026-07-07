import { describe, it, expect, vi } from "vitest";
import { createVideo, listVideos, getVideo } from "../api/client";

const mockJob = {
  id: "job-1",
  url: "https://youtube.com/watch?v=test",
  title: "Test Video",
  status: "queued",
  current_step: "queued",
  video_path: null,
  audio_path: null,
  thumbnail_path: null,
  transcript: null,
  summary: null,
  tags: [],
  chapters: [],
  error: null,
  created_at: "2026-07-07T00:00:00Z",
  updated_at: "2026-07-07T00:00:00Z",
};

describe("createVideo", () => {
  it("sends POST request with correct body", async () => {
    const fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockJob),
    });
    vi.stubGlobal("fetch", fetch);

    const result = await createVideo("https://youtube.com/watch?v=test");

    const callUrl = fetch.mock.calls[0][0];
    const callOpts = fetch.mock.calls[0][1];
    expect(callUrl).toContain("/api/videos");
    expect(callOpts.method).toBe("POST");
    expect(JSON.parse(callOpts.body)).toEqual({
      url: "https://youtube.com/watch?v=test",
    });
    expect(result.id).toBe("job-1");
  });
});

describe("listVideos", () => {
  it("returns array of VideoJobResponse", async () => {
    const fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([mockJob]),
    });
    vi.stubGlobal("fetch", fetch);

    const result = await listVideos();

    const callUrl = fetch.mock.calls[0][0];
    expect(callUrl).toContain("/api/videos");
    expect(Array.isArray(result)).toBe(true);
    expect(result[0].id).toBe("job-1");
  });
});

describe("getVideo", () => {
  it("returns single VideoJobResponse", async () => {
    const fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockJob),
    });
    vi.stubGlobal("fetch", fetch);

    const result = await getVideo("job-1");

    const callUrl = fetch.mock.calls[0][0];
    expect(callUrl).toContain("/api/videos/job-1");
    expect(result.id).toBe("job-1");
  });
});

describe("validation", () => {
  it("throws on invalid response", async () => {
    const fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: "job-1" }), // missing required fields
    });
    vi.stubGlobal("fetch", fetch);

    await expect(getVideo("job-1")).rejects.toThrow();
  });
});
