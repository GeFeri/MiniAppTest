import { api } from "./axiosInstance";
import type { EventItem, ID } from "./types";

// GET /api/events/
export async function getEvents(): Promise<EventItem[]> {
  const r = await api.get("/events/");
  return r.data;
}

// GET /api/events/:id/
export async function getEventById(id: ID): Promise<EventItem> {
  const r = await api.get(`/events/${id}/`);
  return r.data;
}

// POST /api/events/
export async function createEvent(payload: {
  title: string;
  content?: string;
  date: string; // ISO
}): Promise<EventItem> {
  const r = await api.post("/events/", payload);
  return r.data;
}

// PATCH /api/events/:id/
export async function updateEvent(id: ID, payload: Partial<{ title: string; content: string; date: string }>): Promise<EventItem> {
  const r = await api.put(`/events/${id}/`, payload);
  return r.data;
}

// DELETE /api/events/:id/
export async function deleteEvent(id: ID): Promise<void> {
  await api.delete(`/events/${id}/`);
}
