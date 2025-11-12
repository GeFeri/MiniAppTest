// src/api/birthdaysApi.ts
import { api } from "./axiosInstance";
import type { BirthdayUser } from "./types";

// новый — без неиспользуемого аргумента
export async function getBirthdays(): Promise<BirthdayUser[]> {
  const r = await api.get("/birthdays/")
  return r.data
}
