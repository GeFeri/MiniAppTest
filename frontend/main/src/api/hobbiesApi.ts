import { api } from "./axiosInstance";
import type { Hobby, TypeHobby, UserHobby, ID } from "./types";

// ------------------------------
// 🎨 Каталог хобби
// ------------------------------

// GET /api/hobbies/
export async function getHobbies(): Promise<Hobby[]> {
  const r = await api.get("/hobbies/");
  return r.data;
}

// POST /api/hobbies/
export async function createHobby(payload: {
  name: string;
  emoji?: string;
  color?: string;
  type_id?: number;
}): Promise<Hobby> {
  const r = await api.post("/hobbies/", payload);
  return r.data;
}

// GET /api/hobbies/:id/
export async function getHobby(id: ID): Promise<Hobby> {
  const r = await api.get(`/hobbies/${id}/`);
  return r.data;
}

// PUT /api/hobbies/:id/
export async function updateHobby(
  id: ID,
  payload: Partial<{ name: string; emoji: string; color: string; type_id: number }>
): Promise<Hobby> {
  const r = await api.put(`/hobbies/${id}/`, payload);
  return r.data;
}

// DELETE /api/hobbies/:id/
export async function deleteHobby(id: ID): Promise<void> {
  await api.delete(`/hobbies/${id}/`);
}

// ------------------------------
// 🧩 Типы хобби (категории)
// ------------------------------

// GET /api/type-hobbies/
export async function getTypeHobbies(): Promise<TypeHobby[]> {
  const r = await api.get("/type-hobbies/");
  return r.data;
}

// ------------------------------
// 👤 Пользовательские хобби
// ------------------------------

// GET /api/user-hobbies/
export async function getUserHobbies(): Promise<UserHobby[]> {
  const r = await api.get("/user-hobbies/");
  return r.data;
}

// POST /api/user-hobbies/
export async function addUserHobby(payload: {
  hobby_id: ID;
  description?: string;
}): Promise<UserHobby> {
  const r = await api.post("/user-hobbies/", payload);
  return r.data;
}

// DELETE /api/user-hobbies/:hobby_id/
export async function deleteUserHobby(hobby_id: ID): Promise<void> {
  await api.delete(`/user-hobbies/${hobby_id}/`);
}
