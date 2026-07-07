import { z } from "zod";

export const JobStatusSchema = z.enum([
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
]);

export type JobStatus = z.infer<typeof JobStatusSchema>;

export const ChapterSchema = z.object({
  start: z.string().min(1),
  title: z.string().min(1),
});

export type Chapter = z.infer<typeof ChapterSchema>;

export const CreateVideoRequestSchema = z.object({
  url: z.string().min(1),
});

export type CreateVideoRequest = z.infer<typeof CreateVideoRequestSchema>;

export const VideoJobResponseSchema = z.object({
  id: z.string(),
  url: z.string(),
  title: z.string().nullable().optional(),
  status: JobStatusSchema.default("queued"),
  current_step: z.string().default("queued"),
  video_path: z.string().nullable().optional(),
  audio_path: z.string().nullable().optional(),
  thumbnail_path: z.string().nullable().optional(),
  transcript: z.string().nullable().optional(),
  summary: z.string().nullable().optional(),
  tags: z.array(z.string()).default([]),
  chapters: z.array(ChapterSchema).default([]),
  error: z.string().nullable().optional(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export type VideoJobResponse = z.infer<typeof VideoJobResponseSchema>;

export const WorkerMessageSchema = z.object({
  job_id: z.string(),
  video_id: z.string(),
  attempt: z.number().int().default(1),
  url: z.string().optional(),
});

export type WorkerMessage = z.infer<typeof WorkerMessageSchema>;
