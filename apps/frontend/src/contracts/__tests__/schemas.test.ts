import { describe, it, expect } from "vitest";
import {
  JobStatusSchema,
  ChapterSchema,
  CreateVideoRequestSchema,
  VideoJobResponseSchema,
  WorkerMessageSchema,
} from "../schemas";

describe("JobStatusSchema", () => {
  const VALID_STATUSES = [
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

  it("accepts all 10 valid values", () => {
    for (const s of VALID_STATUSES) {
      const result = JobStatusSchema.safeParse(s);
      expect(result.success).toBe(true);
    }
  });

  it("rejects invalid status", () => {
    const result = JobStatusSchema.safeParse("invalid");
    expect(result.success).toBe(false);
  });
});

describe("ChapterSchema", () => {
  it("validates valid chapter", () => {
    const result = ChapterSchema.safeParse({ start: "00:00", title: "Intro" });
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.start).toBe("00:00");
      expect(result.data.title).toBe("Intro");
    }
  });

  it("rejects empty start", () => {
    const result = ChapterSchema.safeParse({ start: "", title: "Intro" });
    expect(result.success).toBe(false);
  });

  it("rejects empty title", () => {
    const result = ChapterSchema.safeParse({ start: "00:00", title: "" });
    expect(result.success).toBe(false);
  });
});

describe("CreateVideoRequestSchema", () => {
  it("validates valid url", () => {
    const result = CreateVideoRequestSchema.safeParse({
      url: "https://youtube.com/watch?v=test",
    });
    expect(result.success).toBe(true);
  });

  it("rejects empty url", () => {
    const result = CreateVideoRequestSchema.safeParse({ url: "" });
    expect(result.success).toBe(false);
  });
});

describe("VideoJobResponseSchema", () => {
  const NOW = "2026-07-06T12:00:00Z";

  it("validates minimal payload with defaults", () => {
    const result = VideoJobResponseSchema.safeParse({
      id: "abc-123",
      url: "https://youtube.com/watch?v=test",
      created_at: NOW,
      updated_at: NOW,
    });
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.status).toBe("queued");
      expect(result.data.current_step).toBe("queued");
      expect(result.data.tags).toEqual([]);
      expect(result.data.chapters).toEqual([]);
    }
  });

  it("validates full payload with all fields", () => {
    const result = VideoJobResponseSchema.safeParse({
      id: "abc-123",
      url: "https://youtube.com/watch?v=test",
      title: "Test Video",
      status: "completed",
      current_step: "completed",
      video_path: "/storage/videos/test.mp4",
      audio_path: "/storage/audio/test.mp3",
      thumbnail_path: "/storage/thumbnails/test.jpg",
      transcript: "Hello world",
      summary: "A test video",
      tags: ["test", "demo"],
      chapters: [{ start: "00:00", title: "Intro" }],
      created_at: NOW,
      updated_at: NOW,
    });
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.tags).toEqual(["test", "demo"]);
      expect(result.data.chapters).toHaveLength(1);
    }
  });

  it("rejects missing id", () => {
    const result = VideoJobResponseSchema.safeParse({
      url: "https://youtube.com/watch?v=test",
      created_at: NOW,
      updated_at: NOW,
    });
    expect(result.success).toBe(false);
  });

  it("rejects invalid status", () => {
    const result = VideoJobResponseSchema.safeParse({
      id: "abc-123",
      url: "https://youtube.com/watch?v=test",
      status: "invalid",
      created_at: NOW,
      updated_at: NOW,
    });
    expect(result.success).toBe(false);
  });
});

describe("WorkerMessageSchema", () => {
  it("validates with defaults", () => {
    const result = WorkerMessageSchema.safeParse({
      job_id: "j1",
      video_id: "v1",
    });
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.attempt).toBe(1);
      expect(result.data.url).toBeUndefined();
    }
  });

  it("validates with url", () => {
    const result = WorkerMessageSchema.safeParse({
      job_id: "j1",
      video_id: "v1",
      url: "https://youtube.com/watch?v=test",
    });
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.url).toBe("https://youtube.com/watch?v=test");
    }
  });

  it("rejects missing job_id", () => {
    const result = WorkerMessageSchema.safeParse({ video_id: "v1" });
    expect(result.success).toBe(false);
  });

  it("rejects missing video_id", () => {
    const result = WorkerMessageSchema.safeParse({ job_id: "j1" });
    expect(result.success).toBe(false);
  });
});
