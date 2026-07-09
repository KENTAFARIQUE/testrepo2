export const QUEUE_VIDEO_DOWNLOAD = "video.download";
export const QUEUE_VIDEO_AUDIO_EXTRACT = "video.audio.extract";
export const QUEUE_VIDEO_THUMBNAIL_GENERATE = "video.thumbnail.generate";
export const QUEUE_VIDEO_TRANSCRIBE = "video.transcribe";
export const QUEUE_VIDEO_SUMMARIZE = "video.summarize";
export const QUEUE_VIDEO_TAGS = "video.tags";
export const QUEUE_VIDEO_FAILED = "video.failed";
export const QUEUE_VIDEO_STATUS = "video.status";

export const ALL_QUEUES = [
  QUEUE_VIDEO_DOWNLOAD,
  QUEUE_VIDEO_AUDIO_EXTRACT,
  QUEUE_VIDEO_THUMBNAIL_GENERATE,
  QUEUE_VIDEO_TRANSCRIBE,
  QUEUE_VIDEO_SUMMARIZE,
  QUEUE_VIDEO_TAGS,
  QUEUE_VIDEO_FAILED,
  QUEUE_VIDEO_STATUS,
] as const;
