import { api } from "./axiosInstance";
import type { ID, InviteKey } from "./types";

// GET /api/invites/
export async function getInvites(): Promise<InviteKey[]> {
  const r = await api.get("/invites/");
  return r.data;
}

// GET /api/invites/:id/
export async function getInvite(id: ID): Promise<InviteKey> {
  const r = await api.get(`/invites/${id}/`);
  return r.data;
}

// POST /api/invites/
export async function createInvite(payload: {
  department: ID;
  first_name?: string;
  last_name?: string;
  telegram_username?: string;
  expires_in_hours?: number;
}): Promise<InviteKey> {
  const r = await api.post("/invites/", payload);
  return r.data;
}

// DELETE /api/invites/:id/
export async function deleteInvite(id: ID): Promise<void> {
  await api.delete(`/invites/${id}/`);
}

// POST /api/invites/activate/
export async function activateInvite(payload: {
  telegram_id: number | string;
  invite_key: string;
  telegram_username?: string;
}): Promise<{ user_id: ID; username: string }> {
  const r = await api.post("/invites/activate/", payload);
  return r.data;
}
