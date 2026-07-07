import {
  VideoJobResponseSchema,
  type VideoJobResponse,
} from "../contracts";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API error ${res.status}: ${body}`);
  }

  return res.json();
}

function validate<T>(data: unknown, schema: { parse: (d: unknown) => T }): T {
  return schema.parse(data);
}

export async function createVideo(url: string): Promise<VideoJobResponse> {
  const data = await request("/api/videos", {
    method: "POST",
    body: JSON.stringify({ url }),
  });
  return validate(data, VideoJobResponseSchema);
}

export async function listVideos(): Promise<VideoJobResponse[]> {
  const data = await request("/api/videos");
  return validate(data, VideoJobResponseSchema.array());
}

export async function getVideo(id: string): Promise<VideoJobResponse> {
  const data = await request(`/api/videos/${id}`);
  return validate(data, VideoJobResponseSchema);
}
