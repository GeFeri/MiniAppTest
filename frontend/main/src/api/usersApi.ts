import { api } from "./axiosInstance";
import type { ID, User } from "./types";

// GET /api/users/
export async function getUsers(search?: string): Promise<User[]> {
  const r = await api.get("/users/", {
    params: search ? { search } : {},
  });
  return r.data;
}

// GET /api/users/:id/
export async function getUser(id: ID): Promise<User> {
  const r = await api.get(`/users/${id}/`);
  return r.data;
}

// GET /api/users/me/
export async function getMe(): Promise<User> {
  const r = await api.get("/users/me/");
  return r.data;
}

// PATCH /api/users/:id/
export async function updateUser(id: ID, payload: Partial<User> & { hobbies_ids?: number[] }): Promise<User> {
  const r = await api.patch(`/users/${id}/`, payload);
  return r.data;
}

// Удобный шорткат: обновить себя
export async function updateMe(payload: Partial<User> & { hobbies_ids?: number[] }): Promise<User> {
  // Обычно у нас нет своего id под рукой — сначала берём me
  const me = await getMe();
  return updateUser(me.id, payload);
}
