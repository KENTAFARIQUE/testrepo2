import { describe, it, expect } from "vitest";
import {
  QUEUE_VIDEO_DOWNLOAD,
  QUEUE_VIDEO_AUDIO_EXTRACT,
  QUEUE_VIDEO_THUMBNAIL_GENERATE,
  QUEUE_VIDEO_TRANSCRIBE,
  QUEUE_VIDEO_SUMMARIZE,
  QUEUE_VIDEO_TAGS,
  QUEUE_VIDEO_FAILED,
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
  });

  it("ALL_QUEUES has 7 values", () => {
    expect(ALL_QUEUES).toHaveLength(7);
  });

  it("ALL_QUEUES has no duplicates", () => {
    expect(new Set(ALL_QUEUES).size).toBe(ALL_QUEUES.length);
  });
});
