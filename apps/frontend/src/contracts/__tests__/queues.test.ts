import { describe, it, expect } from "vitest";
import {
  QUEUE_VIDEO_DOWNLOAD,
  QUEUE_VIDEO_AUDIO_EXTRACT,
  QUEUE_VIDEO_THUMBNAIL_GENERATE,
  QUEUE_VIDEO_TRANSCRIBE,
  QUEUE_VIDEO_SUMMARIZE,
  QUEUE_VIDEO_TAGS,
  QUEUE_VIDEO_FAILED,
  QUEUE_VIDEO_STATUS,
  ALL_QUEUES,
} from "../queues";

describe("queue constants", () => {
  it("all values match expected strings", () => {
    expect(QUEUE_VIDEO_DOWNLOAD).toBe("video.download");
    expect(QUEUE_VIDEO_AUDIO_EXTRACT).toBe("video.audio.extract");
    expect(QUEUE_VIDEO_THUMBNAIL_GENERATE).toBe("video.thumbnail.generate");
    expect(QUEUE_VIDEO_TRANSCRIBE).toBe("video.transcribe");
    expect(QUEUE_VIDEO_SUMMARIZE).toBe("video.summarize");
    expect(QUEUE_VIDEO_TAGS).toBe("video.tags");
    expect(QUEUE_VIDEO_FAILED).toBe("video.failed");
    expect(QUEUE_VIDEO_STATUS).toBe("video.status");
  });

  it("ALL_QUEUES has 8 values", () => {
    expect(ALL_QUEUES).toHaveLength(8);
  });

  it("ALL_QUEUES has no duplicates", () => {
    expect(new Set(ALL_QUEUES).size).toBe(ALL_QUEUES.length);
  });
});
